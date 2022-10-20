from unittest import TestCase, mock

from screener.repositories.institutional_investor import InstitutionalInvestorRepository


class TestInstitutionalInvestorClient(TestCase):
    def test_save__institutional_investor(self):
        mocked_insert = mock.Mock(return_value="inserted")
        mocked_app_mongo_client = mock.Mock(insert=mocked_insert)

        institutional_investor = InstitutionalInvestorRepository(mocked_app_mongo_client)
        inserted_value = institutional_investor.save(mock.Mock(to_dict=lambda: {"_id": "1", "value": "some-dict"}))

        mocked_insert.assert_called_with({"value": "some-dict"})
        self.assertEquals(inserted_value, "inserted")

    @mock.patch("screener.repositories.institutional_investor.get_institutional_investor_activity")
    def test_get_all__institutional_investor(self, mocked_get_institutional_investor_activity):
        mocked_insert = mock.Mock(return_value=[1, 2, 3])
        mocked_app_mongo_client = mock.Mock(find_all=mocked_insert)
        mocked_get_institutional_investor_activity.side_effect = lambda x: x + 10
        institutional_investor = InstitutionalInvestorRepository(mocked_app_mongo_client)

        ii = institutional_investor.get_all()

        self.assertListEqual([11, 12, 13], ii)

    @mock.patch("screener.repositories.institutional_investor.get_institutional_investor_activity")
    def test_get_by_id__institutional_investor(self, mocked_get_institutional_investor_activity):
        mocked_find_by_id = mock.Mock(return_value="some-ii")
        mocked_app_mongo_client = mock.Mock(find_by_id=mocked_find_by_id)
        mocked_get_institutional_investor_activity.side_effect = lambda x: x + "-weird"
        institutional_investor = InstitutionalInvestorRepository(mocked_app_mongo_client)

        ii = institutional_investor.get_by_id("some-id")

        mocked_find_by_id.assert_called_with("some-id")
        self.assertEqual("some-ii-weird", ii)

    @mock.patch("screener.repositories.institutional_investor.get_institutional_investor_activity")
    def test_get_by_id__None__when_ii_data_not_found(self, mocked_get_institutional_investor_activity):
        mocked_app_mongo_client = mock.Mock(find_by_id=lambda x: None)
        mocked_get_institutional_investor_activity.side_effect = lambda x: x + "-weird"
        institutional_investor = InstitutionalInvestorRepository(mocked_app_mongo_client)

        self.assertIsNone(institutional_investor.get_by_id("some-id"))
