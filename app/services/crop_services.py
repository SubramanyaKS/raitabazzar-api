import difflib
from typing import Any, Dict, List, Optional, Tuple

from app.data.crop_master import CROP_SYNONYMS, CROPS_MASTER_DATA
from app.data.data import KARNATAKA_DISTRICT_BENCHMARKS

BENCHMARK_COMMODITY_MAPPING: Dict[str, List[str]] = {
    "tomato": ["Tomato"],
    "onion": ["Onion"],
    "potato": ["Potato"],
    "green_chilli": ["Green Chilli"],
    "beans": ["Beans"],
    "capsicum": ["Capsicum"],
    "cauliflower": ["Cauliflower"],
    "ginger": ["Ginger(Green)", "Ginger"],
    "paddy": ["Paddy(Common)", "Paddy"],
    "ragi": ["Ragi"],
    "maize": ["Maize"],
    "bengal_gram": ["Bengal Gram"],
    "groundnut": ["Groundnut"],
    "banana": ["Banana"],
    "mango": ["Mango"],
    "tender_coconut": ["Tender Coconut"],
    "coconut": ["Coconut", "Copra (Dry Coconut)"],
    "sugarcane": ["Sugarcane"],
    "cotton": ["Cotton"],
    "arecanut": ["Arecanut"],
    "red_chilli": ["Red Chilli"],
}


def _build_matched_synonyms(q_raw: str, crop: Dict[str, Any], synonyms: List[str]) -> List[str]:
    result: List[str] = []
    q_norm = q_raw.strip().lower()

    if q_raw.strip():
        result.append(q_raw.strip())

    kn = crop.get("name_kn", "")
    en = crop.get("name_en", "").split("/")[0].split("(")[0].strip().lower()

    kanglish = next(
        (s for s in synonyms if s.isascii() and s.lower() != en and " " not in s and len(s) > 2),
        None,
    )

    for item in [kn, kanglish, en]:
        if item and item not in result and item.lower() not in [r.lower() for r in result]:
            result.append(item)

    for s in synonyms:
        if len(result) >= 4:
            break
        if s.lower() != q_norm and (q_norm in s.lower() or s.lower() in q_norm):
            if s not in result and s.lower() not in [r.lower() for r in result]:
                result.append(s)

    return result


def find_matching_crop(query: str) -> Optional[Tuple[Dict[str, Any], List[str]]]:
    q_raw = query.strip()
    if not q_raw:
        return None
    q = q_raw.lower()

    # 1. Exact match across id, names, or synonyms
    for crop in CROPS_MASTER_DATA:
        crop_id = crop["id"]
        synonyms = CROP_SYNONYMS.get(crop_id, [])
        all_terms = [
            crop_id,
            crop.get("name_en", "").lower(),
            crop.get("name_kn", ""),
            crop.get("name_hi", ""),
        ] + [s.lower() for s in synonyms]

        if q_raw in (crop.get("name_kn", ""), crop.get("name_hi", "")):
            return crop, _build_matched_synonyms(q_raw, crop, synonyms)

        if q in [t.lower() for t in all_terms if t]:
            return crop, _build_matched_synonyms(q_raw, crop, synonyms)

    # 2. Substring matching
    for crop in CROPS_MASTER_DATA:
        crop_id = crop["id"]
        synonyms = CROP_SYNONYMS.get(crop_id, [])
        all_terms = [
            crop_id,
            crop.get("name_en", "").lower(),
            crop.get("name_kn", ""),
            crop.get("name_hi", ""),
        ] + [s.lower() for s in synonyms]

        for term in all_terms:
            if not term:
                continue
            if len(q) >= 3 and q in term.lower():
                return crop, _build_matched_synonyms(q_raw, crop, synonyms)
            if len(term) >= 4 and term.lower() in q:
                return crop, _build_matched_synonyms(q_raw, crop, synonyms)
            if len(q_raw) >= 2 and (q_raw in term or term in q_raw):
                return crop, _build_matched_synonyms(q_raw, crop, synonyms)

    # 3. Fuzzy matching for transliterations
    all_latin_terms: Dict[str, Dict[str, Any]] = {}
    for crop in CROPS_MASTER_DATA:
        crop_id = crop["id"]
        synonyms = CROP_SYNONYMS.get(crop_id, [])
        latin_syns = [crop_id, crop.get("name_en", "").lower()] + [
            s.lower() for s in synonyms if s.isascii()
        ]
        for term in latin_syns:
            if term:
                all_latin_terms[term] = crop

    closest = difflib.get_close_matches(q, list(all_latin_terms.keys()), n=1, cutoff=0.7)
    if closest:
        crop = all_latin_terms[closest[0]]
        synonyms = CROP_SYNONYMS.get(crop["id"], [])
        return crop, _build_matched_synonyms(q_raw, crop, synonyms)

    return None


def get_benchmark(
    crop_id: str, standard_name: str, district: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    candidate_names = BENCHMARK_COMMODITY_MAPPING.get(crop_id, [standard_name])

    matching_benchmarks = [
        b
        for b in KARNATAKA_DISTRICT_BENCHMARKS
        if any(c.lower() == b.get("commodity", "").lower() for c in candidate_names)
        or any(c.lower() in b.get("commodity", "").lower() for c in candidate_names)
    ]

    if not matching_benchmarks:
        return None

    selected = None
    if district and district.strip():
        dist_clean = district.strip().lower()
        selected = next(
            (b for b in matching_benchmarks if b.get("district", "").lower() == dist_clean),
            None,
        )

    if not selected:
        selected = matching_benchmarks[0]

    return {
        "district": selected.get("district"),
        "market": selected.get("market"),
        "modal_price": float(selected.get("modal_price", 0)),
        "min_price": float(selected.get("min_price", 0)),
        "max_price": float(selected.get("max_price", 0)),
        "unit": selected.get("unit", "Kg"),
    }


def get_master_crops(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns the master list of Karnataka crops, optionally filtered by category.
    """
    data = CROPS_MASTER_DATA
    if category and category.strip().lower() != "all":
        cat_lower = category.strip().lower()
        data = [c for c in data if c["category"].lower() == cat_lower]
    return data


def search_crop(query: str, district: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Performs vernacular search across Kannada, Hindi, English, and Kanglish,
    resolving matched synonyms and district APMC benchmark pricing.
    Returns None if no matching crop is found.
    """
    match_result = find_matching_crop(query)
    if not match_result:
        return None

    crop, matched_synonyms = match_result
    standard_name = crop.get("name_en", "").split("/")[0].split("(")[0].strip()
    benchmark = get_benchmark(crop["id"], standard_name, district=district)

    return {
        "standard_name": standard_name,
        "kannada_name": crop.get("name_kn"),
        "hindi_name": crop.get("name_hi"),
        "category": crop.get("category"),
        "unit": crop.get("default_unit", "Kg"),
        "synonyms_matched": matched_synonyms,
        "benchmark": benchmark,
    }
