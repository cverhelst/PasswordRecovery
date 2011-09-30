To use this password recovery tool
follow the next steps:

########
	- Host a server:
		* Choose if you want to use the tool
	- Connect to a server:
		* Choose if you want to add your pc
		as a node to an existing host
########
	SERVER:
	- Server settings:
		* Here you can see your ip adress and
		change your port through which other
		nodes will connect
	CLIENT:
	- Client settings:
		* Enter the IP adress and the port
		of the host you want to connect to
#######
	SERVER:
	- INFO of elements on the screen:
		1. Recovered passwords:
			A list containing all the
			recovered passwords
		2. Passwords to search for
			A list of either:
				- only hashes
				- contents of a sam file
				-> username:something:hash:...
				   it will use 'hash' as the hash
			that need recovering
				   
			These hashes can be added by copy / paste
			or by the next field:
		3. Adding a password:
			Enter a hash and press 'Add' to add this
			hash to the pool that need recovering
		4. Maximum password length to test for.
				* meaning: length 3 means
				only passwords of 3 characters will
				be generated and tested for
		5. Password length for benchmark:
				* Same as 4. but only during the
				benchmark ( use this to achieve a
				reliable benchmark, meaning, a benchmark
				run time of over 10s preferably )
				* WARNING: Keep this value low,
				in essence it tries every possible password
				using the given parameters as A NORMAL WORK
				with the exception of the password length.
				Setting this value equal to your desired password
				length would nullify it's purpose of
				benchmarking the system with a fraction of the
				needed work.
		6. Charset used in the password:
			sets the range of characters to use for generating
			possible passwords
			possibilities:
				- numeric: 0 - 9
				- alpha: a - z
				- alphanumeric: 0 - z
				- printable: every printable ascii character
				- ascii: every ascii character	
		7. Hashfunction used in password:
			sets the hashfunction to use when generating
			possible passwords
			possibilities:
				- lanman: old windows hashing function
				- sha1
				- sha256
				- sha512
				- MD5
		8. Convert a password to a hash:
			hashes the given password
			* For testing purposes, easy copy-paste into above
			password field
		9. Passwords / sec:
			After running the benchmark this will display the
			achieved passwords / seconds of your system and 
			networked nodes. This represents how many guesses
			the system can try each second against the provided 
			hashes.
				* Used to determine maximum recovery length
				for the given workload
		10. Run benchmark:
			Run the benchmark to get an idea of the time needed
			to recover your passwords.
				* NOTE: The benchmark is always run ( if necessary )
				during the normal workload.
		11. Approximate maximum for the given workload:
			Represents the time it would take for this system and
			networked nodes to recover the password, SHOULD the password
			/ one of the passwords be the very last value to be checked.
			I.E. The system will, very likely and with minimal error, not
			run longer than said time.
				* This approximation is usually higher than the time
				really needed because of overhead in setting up the work.
				* This approximation assumes that the system and networked
				nodes are not taxed any higher than they were during the
				benchmark.
		12. Update expected time with new parameters
			Recalculates the needed time to recover the passwords as
			described above, but with the updated values.
				* This removes the need to run the benchmark again
		13. Progress:
			This represents the time run versus the expected maximum
			time.
		14. Start guessing:
			The name says it all.
		
				
				
				