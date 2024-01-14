import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.util.*;

public class UDPClient{

	public final static int SERVICE_PORT = 2543;
	public static void main(String[] Args) throws IOException{
		try{
			// input
			Scanner sc = new Scanner(System.in);

			System.out.println("client running");
			// initiate client socket  no need to add port on constructor/ bind to a port
			DatagramSocket clientSocket = new DatagramSocket();

			// Get the IP address of the server
      		InetAddress IPAddress = InetAddress.getByName("localhost");

      		// Creating corresponding buffers
      		byte[] sendingDataBuffer = new byte[1024];
      		byte[] receivingDataBuffer = new byte[1024];

      		// Converting data to bytes and storing them in the sending buffer
      		//String sentence = "Hello from UDP client";
      		//sendingDataBuffer = sentence.getBytes();

      		

      		// sending UDP packet to the server
      		//clientSocket.send(sendingPacket);


      		// The while method/strategy

      		while (true){
	            String input = sc.nextLine();
	  
	            // convert the String input into the byte array.
	            sendingDataBuffer = input.getBytes();
	  
	            // Step 2 : Create the datagramPacket for sending
	            // the data.
	            // Creating a UDP packet 
      			DatagramPacket sendingPacket = new DatagramPacket(sendingDataBuffer,sendingDataBuffer.length,IPAddress, SERVICE_PORT);
	  
	            // Step 3 : invoke the send call to actually send
	            // the data.
	            clientSocket.send(sendingPacket);
	  
	            // break the loop if user enters "bye"
	            if (input.equals("bye"))
	                break;
        	}


		}catch(SocketException e){
			e.printStackTrace();
		}

	}
}