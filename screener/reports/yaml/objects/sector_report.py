# todo: fix reporting part
from screener.common import u_yaml


class SectorReport:
    def __init__(self, output_file, ascending=False, sorted_by=None, keep_top_results=None):
        self._ascending = ascending
        self._sorted_by = sorted_by or "less_than_maximum"
        self.output_file = output_file
        self._keep_top_results = keep_top_results

    @staticmethod
    def _get_sectors_as_dict(sectors):
        sectors_as_dict = []
        for sector in sectors:
            try:
                sectors_as_dict.append(sector.to_dict())
            except Exception:
                pass
        return sectors_as_dict

    def generate(self, sectors):
        sectors_as_dict = self._get_sectors_as_dict(sectors)
        sorted_sectors = sorted(
            sectors_as_dict,
            key=lambda sector: sector.get(self._sorted_by, 0),
            reverse=not self._ascending
        )[:self._keep_top_results]
        u_yaml.write(self.output_file, sorted_sectors)
