from typing import Dict, List, TypeVar, Generic, Literal, Any, Optional, Union

from pydantic import BaseModel, Field

from all_types.internal_types import LyrInfoInCtlgSave, PrdcerCtlg
from all_types.request_dtypes import ReqFetchDataset

T = TypeVar("T")


class ResModel(BaseModel, Generic[T]):
    message: str
    request_id: str
    data: T


class ResCostEstimate(BaseModel):
    cost: float
    api_calls: int


class Geometry(BaseModel):
    type: Literal["Point", "Polygon", "MultiPolygon"]
    coordinates: Any


class Feature(BaseModel):
    type: Literal["Feature"]
    properties: dict
    geometry: Geometry


class card_metadata(BaseModel):
    id: str
    name: str
    description: str
    thumbnail_url: str
    catalog_link: str
    records_number: int
    can_access: int


class GeoJson(BaseModel):
    type: Literal["FeatureCollection"]
    features: List[Feature]
    properties:list[str]


class CityData(BaseModel):
    name: str
    lat: float
    lng: float
    borders: Any
    type: str = None


class ResFetchDataset(BaseModel):
    type: Literal["FeatureCollection"]
    features: List[Feature]
    bknd_dataset_id: str
    prdcer_lyr_id: str
    records_count: int
    delay_before_next_call: Optional[int] = 0
    progress: Optional[int] = 0
    next_page_token: Optional[str] = ""


class UserCatalogInfo(PrdcerCtlg):
    prdcer_ctlg_id: str
    ctlg_owner_user_id: str
    thumbnail_url: str


class LayerInfo(BaseModel):
    prdcer_layer_name: str
    prdcer_lyr_id: str
    bknd_dataset_id: str
    points_color: str
    layer_legend: str
    layer_description: str
    records_count: int
    city_name: str
    is_zone_lyr: str
    progress: Optional[int]


class ResLyrMapData(GeoJson, LayerInfo):
    pass


class TrafficCondition(BaseModel):
    start_index: int
    end_index: int
    speed: Optional[str]


class LegInfo(BaseModel):
    start_location: dict
    end_location: dict
    distance: float
    duration: str
    static_duration: str
    polyline: str
    traffic_conditions: List[TrafficCondition]


class RouteInfo(BaseModel):
    origin: str
    destination: str
    route: List[LegInfo]


class NearestPointRouteResponse(BaseModel):
    target: dict
    routes: List[Union[RouteInfo, dict]]


class ResRecolorBasedon(ResLyrMapData):
    sub_lyr_id: str  # This is the additional property


class ResAddPaymentMethod(BaseModel):
    payment_method_id: str
    status: str


class PaymentMethod(BaseModel):
    id: str
    type: str
    details: Dict[str, Any]

class GglPlaceDetails(BaseModel):
    id: str
    name: str
    location: Dict[str, float]
    types: List[str]
    photos: Optional[List[Dict[str, Any]]] = None

class ResGetPaymentMethods(BaseModel):
    payment_methods: List[PaymentMethod]

# types for llm agents
class ResGradientColorBasedOnZoneLLM(BaseModel):
    layers: List[ResRecolorBasedon]
    explanation: str  # This is the additional property


class ResLLMFetchDataset(BaseModel):
    """Extract Location Based Information from the Query"""

    query: str = Field(
        default = "",
        description = "Original query passed by the user."
    )
    is_valid: Literal["Valid", "Invalid"] = Field(
        default="",
        description="Status is valid if the user query is from approved categories and cities. Otherwise, it is invalid."
    )
    reason: str = Field(
        default = "",
        description = """Response message for the User after processing the query. It helps user to identify issues in the query like if city and 
                          place is an approved city or place or not."""
    )

    endpoint: Literal["/fastapi/fetch_dataset"] = "/fastapi/fetch_dataset"

    suggestions : List[str] = Field(
        default = [],
        description = "List of suggestions to improve the query."
    )

    body: Optional[ReqFetchDataset] = Field(
        default=None,
        description="An object containing detailed request parameters for fetching dataset"
    )
    cost: str = Field(
        default = '',
        description = "The cost value returned by calculate_cost_tool"
    )

class ResSrcDistination(BaseModel):
    distance_in_km : float 
    drive_time_in_min : float
    drive_polygon: str

class PopulationViewportData(BaseModel):
    type: str = "FeatureCollection"
    features: List[dict]  # Use dict instead of Feature for flexibility
    properties: list[str] = []
    records_count: int
    zoom_level: int
    min_lng: Optional[float] = None
    min_lat: Optional[float] = None
    max_lng: Optional[float] = None
    max_lat: Optional[float] = None


class ResSalesman(BaseModel):
    success: bool
    request_id: str
    plots: dict[str, str]
    metadata: dict[str, Any]