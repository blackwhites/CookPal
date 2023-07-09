from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import io

class FoodRecognizer:
    def __init__(self, acc_token):
        channel = ClarifaiChannel.get_grpc_channel()
        self.stub = service_pb2_grpc.V2Stub(channel)
        self.metadata = (('authorization', 'Key ' + acc_token),)
        self.userDataObject = resources_pb2.UserAppIDSet(user_id='clarifai', app_id='main')

    def convert_img_to_bytes(self, image):
        image_stream = io.BytesIO()
        image.save(image_stream, format="JPEG")
        image_bytes = image_stream.getvalue()
        image_stream.close()
        return image_bytes

    def recognize(self, image, top_k=3):
        img_bytes = self.convert_img_to_bytes(image)
        post_model_outputs_response = self.stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=self.userDataObject,
                model_id='food-item-recognition',
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            image=resources_pb2.Image(
                                base64=img_bytes
                            )
                        )
                    )
                ]
            ),
            metadata=self.metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

        response = {}
        output = post_model_outputs_response.outputs[0]
        for concept in output.data.concepts[:top_k]:
            response[concept.name] = round(concept.value, 2)

        return response
