import motor.motor_asyncio

DB_URI='mongodb+srv://trungle30902:trungle30902@cloudservice.x5e16ko.mongodb.net/?retryWrites=true&w=majority'

client = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)

database = client.cloud_app