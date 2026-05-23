"""
Layer N — Satellite Decoder Module (Hinengaro / Mind / Pattern)

Normalises satellite source identifiers and frame metadata into a
canonical ``NormalisedFrame`` dict consumed by all engines.

Supported sources: BOM (AUS), Himawari-8 (JPN), GOES-16 (USA), Meteosat (EU).
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class SatelliteSource(str, Enum):
    """Canonical satellite source identifiers."""

    BOM = "BOM"            # Bureau of Meteorology — Australia
    HIMAWARI = "Himawari"  # Himawari-8/9 — Japan
    GOES = "GOES"          # GOES-16 — USA
    METEOSAT = "Meteosat"  # Meteosat — Europe / Africa / Middle East

    @classmethod
    def normalise(cls, raw: str) -> "SatelliteSource":
        """
        Normalise a raw source string to a ``SatelliteSource`` member.

        Accepted aliases (case-insensitive):
        - BOM, bom, Bureau-of-Meteorology  → BOM
        - Himawari, himawari-8, himawari8   → HIMAWARI
        - GOES, goes-16, goes16             → GOES
        - Meteosat, METEOSAT, meteosat-11   → METEOSAT
        """
        mapping: Dict[str, "SatelliteSource"] = {
            "bom": cls.BOM,
            "bureau-of-meteorology": cls.BOM,
            "himawari": cls.HIMAWARI,
            "himawari-8": cls.HIMAWARI,
            "himawari8": cls.HIMAWARI,
            "himawari-9": cls.HIMAWARI,
            "himawari9": cls.HIMAWARI,
            "goes": cls.GOES,
            "goes-16": cls.GOES,
            "goes16": cls.GOES,
            "goes-17": cls.GOES,
            "goes17": cls.GOES,
            "meteosat": cls.METEOSAT,
            "meteosat-11": cls.METEOSAT,
            "meteosat11": cls.METEOSAT,
            "meteosat-10": cls.METEOSAT,
        }
        key = raw.strip().lower()
        source = mapping.get(key)
        if source is None:
            logger.warning(
                "Unknown satellite source %r — defaulting to BOM", raw
            )
            return cls.BOM
        return source


@dataclass
class NormalisedFrame:
    """Canonical representation of a satellite frame."""

    source: SatelliteSource
    region: str
    band: str
    latitude: float
    longitude: float
    pixel_data: str
    raw_source: str  # original string before normalisation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source.value,
            "region": self.region,
            "band": self.band,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "pixel_data": self.pixel_data,
            "raw_source": self.raw_source,
        }


class SatelliteDecoder:
    """
    Decode and normalise satellite frame inputs.

    Usage::

        decoder = SatelliteDecoder()
        frame = decoder.decode(
            satellite_source="himawari-8",
            region="Japan",
            band="VIS",
            pixel_data="<raw>",
            latitude=35.6762,
            longitude=139.6503,
        )
        # frame.source == SatelliteSource.HIMAWARI
    """

    # Default region mapping per satellite (used when region is not provided)
    _DEFAULT_REGIONS: Dict[SatelliteSource, str] = {
        SatelliteSource.BOM: "Southern Pacific",
        SatelliteSource.HIMAWARI: "Asia-Pacific",
        SatelliteSource.GOES: "Americas",
        SatelliteSource.METEOSAT: "Europe-Africa",
    }

    def decode(
        self,
        satellite_source: str,
        region: Optional[str],
        band: str,
        pixel_data: str,
        latitude: float,
        longitude: float,
    ) -> NormalisedFrame:
        """
        Decode raw frame input into a ``NormalisedFrame``.

        Normalises the satellite source identifier and fills in a default
        region if none is provided.
        """
        source = SatelliteSource.normalise(satellite_source)
        resolved_region = region or self._DEFAULT_REGIONS[source]

        frame = NormalisedFrame(
            source=source,
            region=resolved_region,
            band=band,
            latitude=latitude,
            longitude=longitude,
            pixel_data=pixel_data,
            raw_source=satellite_source,
        )
        logger.debug(
            "Decoded frame: source=%s region=%s band=%s",
            source.value,
            resolved_region,
            band,
        )
        return frame
