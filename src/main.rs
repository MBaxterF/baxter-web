#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use eframe;
use eframe::egui;
use egui::{Color32, Key, Rounding};
use egui_extras;
use pyo3::prelude::*;
use pyo3::types::PyTuple;
use std::process::Command;

fn main() {
    let icon = image::open("assets/baxter-factory-icon.png")
        .expect("icon not found")
        .into_rgba8();

    let _ = eframe::run_native(
        "BAXTER Webservice",
        eframe::NativeOptions {
            initial_window_size: Some(egui::vec2(800.0, 600.0)),
            icon_data: Some(eframe::IconData {
                width: icon.dimensions().0,
                height: icon.dimensions().1,
                rgba: icon.into_raw(),
            }),
            ..Default::default()
        },
        Box::new(|cc| Box::new(MarkingPlanGui::new(cc))),
    );
}

struct MarkingPlanGui {
    url: String,
    code: String,
    ga4: bool,
    crawl: String,
}

impl MarkingPlanGui {
    fn new(cc: &eframe::CreationContext<'_>) -> Self {
        let mut fonts = egui::FontDefinitions::default();

        fonts.font_data.insert(
            "oswald".to_owned(),
            egui::FontData::from_static(include_bytes!("../fonts/Oswald-Regular.ttf")),
        );

        fonts
            .families
            .entry(egui::FontFamily::Proportional)
            .or_default()
            .insert(0, "oswald".to_owned());

        let _ = &cc.egui_ctx.set_fonts(fonts);

        Self {
            url: "https://baxter-factory.fr".to_owned(),
            code: "".to_owned(),
            ga4: true,
            crawl: "".to_owned(),
        }
    }
}

impl eframe::App for MarkingPlanGui {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui_extras::install_image_loaders(ctx);

        egui::CentralPanel::default()/*.frame(egui::containers::Frame {
			inner_margin: egui::style::Margin { left: 0., right: 0., top: 0., bottom: 0. },
			outer_margin: egui::style::Margin { left: 0., right: 0., top: 0., bottom: 0. },
			rounding: Rounding { nw: 1.0, ne: 1.0, sw: 1.0, se: 1.0 },
			shadow: eframe::epaint::Shadow { extrusion: 1.0, color: Color32::WHITE },
			fill: Color32::DARK_GRAY,
			stroke: egui::Stroke::new(2.0, Color32::GOLD)
		})*/.show(ctx, |ui| {
			ui.add(egui::Image::new("https://static.wixstatic.com/media/ec84d9_be284b63575c4d5a8a143c099625b129~mv2.png").max_width(200.0).rounding(10.0));
            ui.horizontal(|ui| {
            ui.vertical(|ui| {
			ui.heading("Marking Plan");

			let url_label = ui.label("Url: ");
			let _url = ui.text_edit_singleline(&mut self.url).labelled_by(url_label.id);

			pyo3::prepare_freethreaded_python();

			if ui.button("Générer le code Data Layer").clicked() {
				let data_layer = Python::with_gil(|py| -> PyResult<Py<PyAny>> {
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/html_reader.py")), "html_reader", "html_reader")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/marking_plan.py")), "marking_plan", "marking_plan")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/data_layer.py")), "data_layer", "data_layer")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/mp_reader.py")), "mp_reader", "mp_reader")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/mp_writer.py")), "mp_writer", "mp_writer")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/dl_builder.py")), "dl_builder", "dl_builder")?;

					let app: Py<PyAny> = PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "//py//build_data_layer.py")), "", "")?.getattr("build_data_layer")?.into();
					app.call1(py, PyTuple::new(py, &[self.url.as_str()]))
				});

				self.code = data_layer.unwrap().to_string();

				let xls_file = Python::with_gil(|py| -> PyResult<Py<PyAny>> {
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/html_reader.py")), "html_reader", "html_reader")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/marking_plan.py")), "marking_plan", "marking_plan")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/data_layer.py")), "data_layer", "data_layer")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/mp_reader.py")), "mp_reader", "mp_reader")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/mp_writer.py")), "mp_writer", "mp_writer")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/dl_builder.py")), "dl_builder", "dl_builder")?;

					let app: Py<PyAny> = PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/build_data_layer.py")), "", "")?.getattr("get_file_name")?.into();
					app.call1(py, PyTuple::new(py, &[self.url.as_str()]))
				});

                Command::new("libreoffice").args([xls_file.unwrap().to_string()]).output().expect("failed to open xls");
				//Command::new("excel").args([xls_file.unwrap().to_string()]).output().expect("failed to open xls");
			};

            let mut matomo = false;

            if ui.button("Crawl web page").clicked() {
				let data_layer = Python::with_gil(|py| -> PyResult<Py<PyAny>> {
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/html_reader.py")), "html_reader", "html_reader")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/marking_plan.py")), "marking_plan", "marking_plan")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/data_layer.py")), "data_layer", "data_layer")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/mp_reader.py")), "mp_reader", "mp_reader")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/mp_writer.py")), "mp_writer", "mp_writer")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/dl_builder.py")), "dl_builder", "dl_builder")?;

					let app: Py<PyAny> = PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/crawl.py")), "", "")?.getattr("crawl_web_page")?.into();
					app.call1(py, PyTuple::new(py, &[self.url.as_str()]))
				});

				self.crawl = data_layer.unwrap().to_string();
			};

            ui.add(egui::TextEdit::multiline(&mut self.crawl));
            });

            ui.vertical(|ui| {
			let code_label = ui.label("Code: ");
			let _code = ui.text_edit_multiline(&mut self.code).labelled_by(code_label.id);

			if ctx.input(|i| i.key_down(Key::Enter)) {
				let data_layer = Python::with_gil(|py| -> PyResult<Py<PyAny>> {
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/html_reader.py")), "html_reader", "html_reader")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/marking_plan.py")), "marking_plan", "marking_plan")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/data_layer.py")), "data_layer", "data_layer")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/mp_reader.py")), "mp_reader", "mp_reader")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/mp_writer.py")), "mp_writer", "mp_writer")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/dl_builder.py")), "dl_builder", "dl_builder")?;

					let app: Py<PyAny> = PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/build_data_layer.py")), "", "")?.getattr("build_data_layer")?.into();
					app.call1(py, PyTuple::new(py, &[self.url.as_str()]))
				});

				self.code = data_layer.unwrap().to_string();

				let xls_file = Python::with_gil(|py| -> PyResult<Py<PyAny>> {
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/html_reader.py")), "html_reader", "html_reader")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/marking_plan.py")), "marking_plan", "marking_plan")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/data_layer.py")), "data_layer", "data_layer")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/mp_reader.py")), "mp_reader", "mp_reader")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/mp_writer.py")), "mp_writer", "mp_writer")?;
					PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/dl_builder.py")), "dl_builder", "dl_builder")?;

					let app: Py<PyAny> = PyModule::from_code(py, include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/py/build_data_layer.py")), "", "")?.getattr("get_file_name")?.into();
					app.call1(py, PyTuple::new(py, &[self.url.as_str()]))
				});

				ui.ctx().request_repaint();

                Command::new("libreoffice").args([xls_file.unwrap().to_string()]).output().expect("failed to open xls");
				//Command::new("excel").args([xls_file.unwrap().to_string()]).spawn().expect("failed to open xls");
			}
		});
        });
    });
    }
}
