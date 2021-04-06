import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;

public class UDPServer{

	public final static int SERVICE_PORT = 2543;
	public static void main(String[] Args) throws IOException{
		
		try{
			System.out.println("Server running");
			//THE DATAGRAM socket will receive packet from the client 
			DatagramSocket ds = new DatagramSocket(SERVICE_PORT);

			// Buffers temporarly hold data
			byte[] receivingDataBuffer = new byte[60000];
			byte[] sendingDataBuffer = new byte[60000];

			//UDP packet to store the client data using the buffer for receiving data
			DatagramPacket inputPacket = null;
			


      		while (true){
  
	            // Step 2 : create a DatgramPacket to receive the data.
	            inputPacket = new DatagramPacket(receivingDataBuffer, receivingDataBuffer.length);
	  
	            // Step 3 : revieve the data in byte buffer.
	            // Receive data from the client and store in inputPacket
      			ds.receive(inputPacket);

      			// Printing out the client sent data
      			String receivedData = new String(inputPacket.getData());
      			System.out.println("Sent from the client: "+receivedData);
	           
	  
	            // Exit the server if the client sends "bye"
	            if (receivedData.equals("bye")){
	                System.out.println("Client sent bye.....EXITING");
	                break;
	            }
	  
	            // Clear the buffer after every message.
	            receivingDataBuffer = new byte[60000];
        	}
        }catch(SocketException e){
			e.printStackTrace();
		}
	}

	public static StringBuilder data(byte[] a){
        if (a == null)
            return null;
        StringBuilder ret = new StringBuilder();
        int i = 0;
        while (a[i] != 0){
            ret.append((char) a[i]);
            i++;
        }
        return ret;
    }
}