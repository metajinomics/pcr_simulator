//usage: java pcr primer.txt seq_file.fa
import java.io.*;
import java.util.*;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
class pcr {
	public static void main(String[] args) {
        DateFormat dateformat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
        Date date1 = new Date();
        System.out.println("program START at " + dateformat.format(date1));
        
        //read primer
        String fileName1 = args[0];
		ArrayList <String> PrimerF = new ArrayList<String> ();
		ArrayList <String> PrimerR = new ArrayList<String> ();
		
		ArrayList <String> PrimerFcr = new ArrayList<String> ();
		ArrayList <String> PrimerRcr = new ArrayList<String> ();
		read_primer(fileName1,PrimerF,PrimerR,PrimerFcr,PrimerRcr);
		//System.out.println(PrimerR);
		
        //read seq and running PCR
        String fileName2 = args[1];
        Scanner fileScanner2 = null;
		try {
			fileScanner2 = new Scanner(new File(fileName2));
		} catch(FileNotFoundException e) {
			System.err.println("Could not find file '" + fileName2 + "'.");
			System.exit(1);
		}//try
		
		String line = null;
		
		int readflag = 0;
		StringBuilder seq = new StringBuilder();
		int findcount = 0;
		int total = 0;
		String tempSeq = "";
		while(fileScanner2.hasNext()) {
			line = fileScanner2.nextLine();
			if(line.equals("")){continue;}
			if(line.substring(0,1).equals(">")){
				total++;
				if(readflag == 0){
					readflag = 1;
					continue;
				}else if(readflag == 1){
					tempSeq = seq.toString();
					if(pcrRun (PrimerF,PrimerR,PrimerFcr,PrimerRcr,tempSeq)){findcount++;};
					seq = new StringBuilder();
				}
			}else{
				seq.append(line);
			}
			
			if(!fileScanner2.hasNext()){
				tempSeq = seq.toString();
				if(pcrRun (PrimerF,PrimerR,PrimerFcr,PrimerRcr,tempSeq)){findcount++;};
			}

		}
       	fileScanner2.close();

        System.out.println(findcount);
        System.out.println(total);
        float percent = (float)findcount*100/(float)total;
        System.out.printf("%.2f",percent);
        System.out.println("% sequences are found");
        
        Date date2 = new Date();
        long time = (date2.getTime() - date1.getTime())/1000;
        System.out.println("program DONE in " + time + " secs");
        System.out.println();
        
    }
    
    public static void read_primer (String fileName1,ArrayList <String> PrimerF,ArrayList <String> PrimerR,ArrayList <String> PrimerFcr,ArrayList <String> PrimerRcr) {
    	Scanner fileScanner = null;
    	try {
			fileScanner = new Scanner(new File(fileName1));
		} catch(FileNotFoundException e) {
			System.err.println("Could not find file '" + fileName1 + "'.");
			System.exit(1);
		}//try
		String line = null;
		String Split = ":";
		while(fileScanner.hasNext()) {
			line = fileScanner.nextLine();
			if(line.substring(0,1).equals(">")){
				String[] entry = line.split(Split);
				line = fileScanner.nextLine();
				String primer = line.toUpperCase();
				if(entry[0].equals(">F")){
					PrimerF.add(primer);
					PrimerFcr.add(complement(primer));
				}else if(entry[0].equals(">R")){
					PrimerRcr.add(primer);
					primer = complement(primer);
					PrimerR.add(primer);
				}else{
					System.out.println("Direction need to be specified");
				}
			}
		}
		fileScanner.close();
    }
    
    public static String complement (String primer) {
    	//change order
    	char[] chars = primer.toCharArray();
    	char[] newchars = new char[chars.length];
    	for (int i = 0; i < chars.length; i++) {
			newchars[i] = chars[chars.length-i-1];
    		//change letter
    		if(newchars[i]=='A'){
				newchars[i]='T';
    		}else if(newchars[i]=='T'){
				newchars[i]='A';
    		}else if(newchars[i]=='C'){
				newchars[i]='G';
    		}else if(newchars[i]=='G'){
				newchars[i]='C';
    		}
    	}
		return String.valueOf(newchars);
	} 
	
	public static boolean pcrRun (ArrayList <String> PrimerF,ArrayList <String> PrimerR,ArrayList <String> PrimerFcr,ArrayList <String> PrimerRcr,String contig) {
    	boolean found = false;
    	for(int i =0; i<PrimerF.size();i += 1){
    		int intIndex = 0;
        	intIndex = contig.indexOf(PrimerF.get(i));
        	if(intIndex == -1){continue;}
        	int contlength = 500;
        	int endlengh = intIndex+contlength;
        	
        	if(endlengh > contig.length()){ 
        		endlengh = contig.length();
        	}
        	String Tempcontig = contig.substring(intIndex,endlengh);
        	for (int j=0; j<PrimerR.size();j++){
        		intIndex = Tempcontig.indexOf(PrimerR.get(j));
        		if(intIndex == -1){continue;}
				found = true;
			}
		}
		//this is for reverse complement
		for(int i=0;i<PrimerRcr.size();i++){
			int intIndex = 0;
        	intIndex = contig.indexOf(PrimerRcr.get(i));
        	if(intIndex == -1){continue;}
        	int contlength = 500;
        	int endlengh = intIndex+contlength;
        	
        	if(endlengh > contig.length()){ 
        		endlengh = contig.length();
        	}
        	String Tempcontig = contig.substring(intIndex,endlengh);
        	for (int j=0; j<PrimerFcr.size();j++){
        		intIndex = Tempcontig.indexOf(PrimerFcr.get(j));
        		if(intIndex == -1){continue;}
				found = true;
			}
		}
		return found;
	} 
}
