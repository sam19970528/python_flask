
def get_session_interface():
  from app import create_session
  session = create_session()
  return session

def get_img_folder():
  from app import img_folder
  return img_folder