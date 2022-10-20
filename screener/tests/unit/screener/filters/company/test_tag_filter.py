from unittest import TestCase, mock

from screener.filters.stock.tag_filter import tag_filter_operation, tag_enrich_operation


class TagTest(TestCase):
    def test_tag_filter_operation(self):
        tags = ["a", "b"]
        stock = mock.Mock(has_tags=lambda x: x == tags)

        self.assertTrue(tag_filter_operation(stock, tags))

    @staticmethod
    def test_tag_enrich_operation():
        tags = ["a", "b"]
        update_report_in_metadata = mock.Mock()
        stock = mock.Mock(get_tags=lambda: tags,
                          update_report_in_metadata=update_report_in_metadata)

        tag_enrich_operation(stock)
        update_report_in_metadata.assert_called_with({
            "tags": tags
        })
