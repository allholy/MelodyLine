MelodyLine : MIRLC2 {

	init{|j|
		cmd.postln;
		
		// 1. load 
		~ip = "127.0.0.1";
		~port = 57120;

		~path = "/mnt/DATA/thesis/code/mirlc2/"; //general path
		~pypath = (~path.asString +/+ "python/"); //spesific path for the file that python

		// 2. make paths 
		File.mkdir(~pypath); //create the path if it does not exist
		//(PathName( ~path.asString +/+ "python/")).postln
		~sounds = File( (~pypath.asString+/+"soundnames_analysis.txt").standardizePath, "a" );
		//f.write("The names of the files that will be analyzed: \n");
		
		// start listening on
		if ( thisProcess.openUDPPort(~port),
			{
				~osc = NetAddr(~ip, ~port);

				OSCdef.new(\receive, {
					arg msg;
					msg.postln;
					// ~sorted_path_list = msg[1];
					// ~a.set(\gatef, msg[1]);
				}, '/py', nil, 57120);
			},

			{"Problem with UDP port.".postln}
		)
		"all good to start".postln;
	}

	


	*new { | tag, shape, midi, tilt, size=50, duration=30, confidence=0.8  |
		this.anotherClassMethod(argument)

		// send FS query 
		
		//FSSound.textSearch(query, filter, sort, params, action)
		FSSound.textSearch(query: tag, filter: , params: ('page': 1))
		if ( size < 50 or size > 150,
			{ postln("ERROR: Invalid value for size.") }, {}
		)

		~sounds.write(snd["name"].asString ++ " \n");
		postln (snd["name"].asString++"POST");

		~data.write(shape++" \n"++tilt++" \n"++midi)

		if ( p.isNil,
			{  postln("ERROR: There was a problem downloading this sound.\nINFO: Please try again.");  },
			{

				size.do { |index|
					snd = p[index];
					postln("INFO: Found sound, id: " ++ snd["id"] ++ "name: " ++ snd["name"]);

					//-----------------
					~f.write(snd["name"].asString ++ " \n");
					postln (snd["name"].asString++"POST");
					//-----------------

					this.id(snd.id, 1); // so that each sound is loaded & directly played
				}
			}); // End IF p.isNil
	}
	~sounds.close;
			
	*next { | argument |
		this.
		"hello next".postln;
	}


}
