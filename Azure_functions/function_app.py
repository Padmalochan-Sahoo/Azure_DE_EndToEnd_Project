import azure.functions as func
import logging
import json

app = func.FunctionApp()

# Event Hub Trigger Function
@app.function_name(name="EventHubTrigger1")
@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="o2arena_data",
                               connection="projectevent_RootManageSharedAccessKey_EVENTHUB")
@app.cosmos_db_output(arg_name="cosmosdbOut", database_name="my-database", collection_name="my-container", container_name="my-container", connection="CosmosDbConnectionString")
def eventHub_trigger_func(azeventhub: func.EventHubEvent, cosmosdbOut: func.Out[func.Document]):
    try:
        # Parse the JSON data from the event
        data = azeventhub.get_body().decode('utf-8')
        event_data = json.loads(data)
 
        # Extract relevant information
        user_id = event_data.get("user_id")
        user_name = event_data.get("user_name")
        device_id = event_data.get("device_id")
        device_source = event_data.get("device_source")
        latitude = event_data.get("latitude")
        longitude = event_data.get("longitude")
        entry_time = event_data.get("entry_time")
        exit_time = event_data.get("exit_time")
        store_type = event_data.get("store_type")
        bill_amount = event_data.get("bill_amount")
        payment_mode = event_data.get("payment_mode")
        review_to_store = event_data.get("review_to_store")
        
        # Log the extracted information
        logging.info(f"Received data for user {user_name} (ID: {user_id}) from device {device_source}.")
 
        # Optionally, you can perform additional processing or validation here
 
        # Create a document to be stored in Cosmos DB
        cosmos_document = {
            "id": user_id,
            "user_name": user_name,
            "device_id": device_id,
            "device_source": device_source,
            "latitude": latitude,
            "longitude": longitude,
            "entry_time": entry_time,
            "exit_time": exit_time,
            "store_type":store_type ,
            "bill_amount":bill_amount,
            "payment_mode": payment_mode,
            "review_to_store":review_to_store

        }
 
        # Store the document in Cosmos DB
        cosmosdbOut.set(func.Document.from_dict(cosmos_document))
 
    except Exception as e:
        logging.error(f"Error processing event data: {str(e)}")