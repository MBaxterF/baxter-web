from data_layer import DataLayer, DLObject
from marking_plan import MarkingPlan


class DLBuilder:
    def __init__(self):
        self.__data_layers = []

    def build(self, marking):
        for i in range(marking.count()):
            dl = DataLayer(marking.get_index(i)[0])

            if 'page_view' in marking.get_index(i)[0]:
                dl.put_variable('page_type', 'page_type')

            if 'clic' in marking.get_index(i)[3] and 'recherche' not in marking.get_index(i)[3] \
                    and 'newsletter' not in marking.get_index(i)[3]:
                dl.put_variable('method', 'method')

            if 'search' in marking.get_index(i)[3]:
                dl.put_variable('results', 'results')
                dl.put_variable('search_term', 'search_term', False)

            if 'share' in marking.get_index(i)[0]:
                dl.put_variable('content_type', 'content_type')
                dl.put_variable('item_id', 'item_id')

            if ('view' in marking.get_index(i)[0] and  marking.get_index(i)[0] != 'page_view') or 'select_item'\
                    in marking.get_index(i)[0] or 'add_to_chart' in \
                    marking.get_index(i)[0] or 'chart' in marking.get_index(i)[0]\
                    or 'checkout' in marking.get_index(i)[0] or 'shipping' in marking.get_index(i)[0]:
                items = DLObject('items')
                items.put_variable('item_name', 'item_name')
                items.put_variable('item_id', 'item_id')
                items.put_variable('coupon', 'coupon')
                items.put_variable('discount', 'discount')
                items.put_variable('item_brand', 'item_brand')
                items.put_variable('item_category', 'item_category')
                items.put_variable('item_category2', 'item_category2')
                items.put_variable('item_category3', 'item_category3')
                items.put_variable('item_category4', 'item_category4')
                items.put_variable('item_category5', 'item_category5')
                items.put_variable('item_variant', 'item_variant')
                items.put_variable('location_id', 'location_id')
                items.put_variable('price', 'price')
                items.put_variable('quantity', 'quantity')

                dl.put_object(items)

            self.__data_layers.append(dl)

    def render(self, idx):
        return str(self.__data_layers[idx])

    def render_all(self):
        _str = ""

        for i in range(len(self.__data_layers)):
            _str += self.render(i) + "\n"

        return _str
