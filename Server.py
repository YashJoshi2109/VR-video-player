import socket
import cv2
import pickle
import struct

# Function to play and stream video frames to client and server
def play_and_stream_video(client_socket, server_window_name):
    # Open the MP4 file for reading
    vid = cv2.VideoCapture('720p.mp4')  # Replace with the actual path to your MP4 video
    while vid.isOpened():
        ret, frame = vid.read()
        if not ret:
            break
        frame = cv2.resize(frame, (640, 480))
        data = pickle.dumps(frame)
        message = struct.pack("Q", len(data)) + data
        
        # Send the frame to the client
        client_socket.sendall(message)
        
        # Display the frame in the server window
        cv2.imshow(server_window_name, frame)
        cv2.waitKey(1)  # Needed to update the display
    
    vid.release()

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)

# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        # Create a window for displaying video on the server side
        cv2.namedWindow('Server Video')
        
        # Play and stream video to client and server simultaneously
        play_and_stream_video(client_socket, 'Server Video')
        
        client_socket.close()
        cv2.destroyAllWindows()
