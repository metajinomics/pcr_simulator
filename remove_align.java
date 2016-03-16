import java.io.*;
import java.util.*;

class RemoveAlign {
	public static void main(String[] args) {
        
        //read primer
        String fileName1 = args[0];
        
        Scanner fileScanner = null;
        PrintStream resultOut = null;
		try {
			fileScanner = new Scanner(new File(fileName1));
			resultOut = new PrintStream(args[1]);
		} catch(FileNotFoundException e) {
			System.err.println("Could not find file '" + fileName1 + "'.");
			System.exit(1);
		}//try
		String line = null;
		ArrayList <String> PrimerList = new ArrayList<String> ();
		
		String seq = "";
		int readflag = 0;
		while(fileScanner.hasNext()) {
			line = fileScanner.nextLine();
			if(line.substring(0,1).equals(">")){
				
				if(readflag == 0){
					readflag = 1;
					resultOut.println(line);
					continue;
				}else if(readflag == 1){
					resultOut.println(seq);
					resultOut.println(line);
					seq = "";
				}
			}else{
				//remove dash!!
				seq = seq + line;
				seq = seq.replace("-","");
			}
			if(!fileScanner.hasNext()){
				resultOut.println(seq);
			}
		}
		fileScanner.close();   
    }
}
