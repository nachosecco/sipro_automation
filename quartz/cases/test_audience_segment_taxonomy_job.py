import unittest
from _decimal import Decimal

from core.audience_segment_taxonomy_job import AudienceSegmentTaxonomyJob


class TestAudienceSegmentTaxonomyJob(unittest.TestCase):

    def test_load_taxonomy_to_db(self):
        """Given a taxonomy file of 2 elements test that after job execution,
        those 2 elements are in the db correctly."""
        with AudienceSegmentTaxonomyJob() as job_under_test:
            content = [
                {
                    "segment_id": "1111111111",
                    "cpm": 1.25
                },
                {
                    "segment_id": "2222222222",
                    "cpm": 1.0
                }
            ]
            job_under_test.add_lr_taxonomy_file(content)
            job_under_test.execute()
            taxonomy_record_1 = job_under_test.get_segment("1111111111")
            taxonomy_record_2 = job_under_test.get_segment("2222222222")
            self.assertEqual(len(taxonomy_record_1), 1)
            self.assertEqual(taxonomy_record_1[0]['segment_id'], "1111111111")
            self.assertEqual(taxonomy_record_1[0]['cpm'], Decimal("1.25"))
            self.assertEqual(len(taxonomy_record_2), 1)
            self.assertEqual(taxonomy_record_2[0]['segment_id'], "2222222222")
            self.assertEqual(taxonomy_record_2[0]['cpm'], Decimal("1.0"))

    def test_should_load_unique_segments_one_file_in_db(self):
        """Given a taxonomy file of 2 elements, one of them repeated, test that after job execution,
        there is only 1 element in the db."""
        with AudienceSegmentTaxonomyJob() as job_under_test:
            content = [
                {
                    "segment_id": "1111111111",
                    "cpm": 1.25
                },
                {
                    "segment_id": "1111111111",
                    "cpm": 1.25
                }
            ]
            job_under_test.add_lr_taxonomy_file(content)
            job_under_test.execute()
            taxonomy_record_1 = job_under_test.get_segment("1111111111")
            self.assertTrue(taxonomy_record_1)
            self.assertEqual(len(taxonomy_record_1), 1)
            self.assertEqual(taxonomy_record_1[0]['segment_id'], "1111111111")
            self.assertEqual(taxonomy_record_1[0]['cpm'], Decimal("1.25"))

    def test_should_update_repeated_segments_multiple_files_in_db(self):
        """Given 2 taxonomy files with repeated elements, test that after job execution,
        there is only 1 element in the db."""
        with AudienceSegmentTaxonomyJob() as job_under_test:
            content = [
                {
                    "segment_id": "1111111111",
                    "cpm": 1.25
                }
            ]
            job_under_test.add_lr_taxonomy_file(content)
            job_under_test.execute()

            with AudienceSegmentTaxonomyJob() as job_under_test2:
                content = [
                    {
                        "segment_id": "1111111111",
                        "cpm": 1.20
                    }
                ]
                job_under_test2.add_lr_taxonomy_file(content)
                job_under_test2.execute( skip_db_clean=True)

                taxonomy_record_1 = job_under_test.get_segment("1111111111")
                self.assertTrue(taxonomy_record_1)
                self.assertEqual(len(taxonomy_record_1), 1)
                self.assertEqual(taxonomy_record_1[0]['segment_id'], "1111111111")
                self.assertEqual(taxonomy_record_1[0]['cpm'], Decimal("1.20"))
    def test_load_segments_taxonomy_updates_audience_cpm(self):
        """Given a taxonomy file with 1 element, and an audience expression containing that segment,
        test that after job execution, min and max CPM is updated."""
        with AudienceSegmentTaxonomyJob() as job_under_test:
            content = [
                {
                    "segment_id": "1111111111",
                    "cpm": 1.25
                }
            ]
            job_under_test.add_lr_taxonomy_file(content)
            job_under_test.add_audience(1, 'XXXXX', b'\x08\x01\x1a\n1111111111')
            job_under_test.execute(skip_db_clean=True)
            audience = job_under_test.get_audience('XXXXX')
            self.assertEqual(len(audience), 1)
            self.assertEqual(audience[0]['max_cpm'], Decimal('1.25'))
            self.assertEqual(audience[0]['min_cpm'], Decimal('1.25'))
