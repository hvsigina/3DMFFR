import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class landmark():
    def __init__(self, model_path=None):
        if model_path is None:
        self.model_path = './models/face_landmarker.task'

    def single_image(self, image_path):


baseOptions = mp.tasks.BaseOptions
faceLandmarker = mp.tasks.vision.FaceLandmarker
faceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
visionRunningMode = mp.tasks.vision.RunningMode

landmarkOptions = faceLandmarkerOptions(
    base_options=baseOptions(model_asset_path=self.model_path),
    running_mode=visionRunningMode.IMAGE)

with faceLandmarker.create_from_options(landmarkOptions) as landmarker:
image = mp.Image.create_from_file(image_path)
faceLandmark = landmarker.detect(image)
print(faceLandmark)


def draw_landmarks_on_image(rgb_image, detection_result):


face_landmarks_list = detection_result.face_landmarks
annotated_image = np.copy(rgb_image)

# Loop through the detected faces to visualize.
for idx in range(len(face_landmarks_list)):
face_landmarks = face_landmarks_list[idx]

# Draw the face landmarks.
face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
face_landmarks_proto.landmark.extend([
    landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
])

solutions.drawing_utils.draw_landmarks(
    image=annotated_image,
    landmark_list=face_landmarks_proto,
    connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
    landmark_drawing_spec=None,
    connection_drawing_spec=mp.solutions.drawing_styles
    .get_default_face_mesh_tesselation_style())
solutions.drawing_utils.draw_landmarks(
    image=annotated_image,
    landmark_list=face_landmarks_proto,
    connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
    landmark_drawing_spec=None,
    connection_drawing_spec=mp.solutions.drawing_styles
    .get_default_face_mesh_contours_style())
solutions.drawing_utils.draw_landmarks(
    image=annotated_image,
    landmark_list=face_landmarks_proto,
    connections=mp.solutions.face_mesh.FACEMESH_IRISES,
    landmark_drawing_spec=None,
    connection_drawing_spec=mp.solutions.drawing_styles
    .get_default_face_mesh_iris_connections_style())

return annotated_image

land = landmark()
land_result = land.single_image("E:/WORKSPACE/3DMFFR/output/22_4.jpg")
land_result.
print(land_result)
