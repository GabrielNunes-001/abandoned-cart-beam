import apache_beam as beam
import apache_beam.transforms.userstate as userstate
import json
from datetime import datetime, timedelta


class DetectarAbandono(beam.DoFn):
    BASKET_STATE = beam.transforms.userstate.ReadModifyWriteStateSpec(
        "basket",
        beam.coders.StrUtf8Coder()
    )
    CUSTOMER_STATE = beam.transforms.userstate.ReadModifyWriteStateSpec(
        "customer",
        beam.coders.StrUtf8Coder()
    )
    
    PRODUCT_STATE = beam.transforms.userstate.ReadModifyWriteStateSpec(
        "product",
        beam.coders.StrUtf8Coder()
    )
    
    BASKET_TIMER = beam.transforms.userstate.TimerSpec(
        "basket_timer",
        beam.TimeDomain.WATERMARK
    )
    
    def process(
        self,
        element,
        basket_state=beam.DoFn.StateParam(BASKET_STATE),
        customer_state=beam.DoFn.StateParam(CUSTOMER_STATE),
        basket_timer=beam.DoFn.TimerParam(BASKET_TIMER),
        product_state=beam.DoFn.StateParam(PRODUCT_STATE)
    ):
        customer = element[0]
        evento = element[1]
        
        if evento["page"] == "basket":
            basket_state.write(evento["timestamp"])
            customer_state.write(customer)
            product_state.write(evento["product"])
            horario_basket = datetime.strptime(
                evento["timestamp"],
                "%Y-%m-%d %H:%M:%S"
            )
            horario_limite = horario_basket + timedelta(minutes=10)
            basket_timer.set(horario_limite.timestamp())
            
        elif evento["page"] == "product":
            basket_timer.clear()
            basket_state.clear()
            customer_state.clear()
            product_state.clear()
            
        elif evento["page"] == "checkout":
            basket_timer.clear()
            basket_state.clear()
            customer_state.clear()
            product_state.clear()
                    
    @userstate.on_timer(BASKET_TIMER)
    def verificar_timer(
        self,
        basket_state=beam.DoFn.StateParam(BASKET_STATE),
        customer_state=beam.DoFn.StateParam(CUSTOMER_STATE),
        product_state=beam.DoFn.StateParam(PRODUCT_STATE)
    ):
        timestamp_basket = basket_state.read()
        customer = customer_state.read()
        product = product_state.read()
        
        if timestamp_basket:
            yield {
                "timestamp": timestamp_basket,
                "customer": customer,
                "product": product
            }
            basket_state.clear()
            customer_state.clear()
            product_state.clear()
            
               
with beam.Pipeline() as pipeline:
    events = pipeline | beam.io.ReadFromText("input/page-views.json")

    events = events | beam.Map(json.loads)
    
    events = events | beam.Map(lambda events: (events["customer"], events))
        
    events = events | beam.ParDo(DetectarAbandono())
    
    events = events | beam.Map(json.dumps)
    
    events | beam.io.WriteToText("output/abandoned-carts")