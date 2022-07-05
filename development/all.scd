(
// 1. give ip/ports & paths
~ip = "127.0.0.1";
~port = 57120;

~path = "/mnt/DATA/thesis/code/mirlc2/"; //general path
~pypath = (~path.asString +/+ "python/"); //spesific path for the file that python

// 2. make paths 
File.mkdir(~pypath); //create the path if it does not exist
~audiofiles = ~pypath.asString+/+"soundnames_analysis.txt"
~data = ~pypath.asString+/+"shape.txt"
~f = File( ~audiofiles.standardizePath, "a" ); //open file for appending 

~soundnames = File( (~pypath.asString+/+"soundnames_analysis.txt").standardizePath, "a" );

Freesound.token="hjk2EJjVAGO4HwGrxhoBf5uhCabuDN5Lm4o1C66S";
)

//USER
~tag="music"
~size=50 
~confidence=0.8
~fake = "/mnt/DATA/thesis/code/mirlc2/"; //general path


~shapes = ['asc', 'desc', 'delta', 'rdelta', 'straight' ]

// send FS query
// https://freesound.org/apiv2/search/text/?query=bird&page_size=50&filter=ac_note_confidence:[0.8 TO 1]
FSSound.textSearch(query: ~tag, params: ('page': 1), filter: "ac_note_confidence:[0.8 TO 1]",
			{
				postln("ERROR: There was a problem downloading.");
			}, {

				~size.do { |idx|
					~snd = p[idx];
					postln("INFO: Found sound by tag, id: " ++ ~snd["id"]);

					~f.write(~snd["name"].asString ++ " \n");
					postln (~snd["name"].asString++"POST");
					
				}
				postln ("DONE");
				
			}); //WHAT TO DO
	});	

~f.close;

~listing = ("python3 /mnt/DATA/thesis/pycode/main_script.py " ++ ~soundnames.asString ++ " " ++ ~audiofiles.asString ++ ~data.asString).unixCmdGetStdOut;

// start listening on / OSC
if ( thisProcess.openUDPPort(~port),
	{
		~osc = NetAddr(~ip, ~port);

		OSCdef.new(\receive,
			{
				arg msg;
				msg.postln;
				~sorted_list = msg[1];
				~sorted_list.postln;
			},
			'/py', nil, 57120);
	},
	{"Problem with UDP port.".postln}
)

// check query
if ( size < 50 or size > 150,
	{ postln("ERROR: Invalid value for size.") }, {}
)

//
postln (snd["name"].asString++"POST");
~f.write(snd["name"].asString ++ " \n");



~sorted_list = [2,2,3];

~sampleBufs = List.newClear(0); 
~sorted_list.do{
	arg file;
	~sampleBufs.add(Buffer.read(s, file));
};

PlayBuf.ar(1, ~sampleBufs[0], BufRateScale.kr(bufnum))


List['a', 'b', 'c'].do({ arg item, i; [i, item].postln; });
