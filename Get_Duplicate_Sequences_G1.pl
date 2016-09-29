#use strict;
use Bio::SeqIO;

print "Enter fasta file name:";
my $File_input = <STDIN>;
#@all_files = glob ("*.fasta");
#foreach $eachfile(@all_files)
#{
#	chomp $eachfile;
#	$File_input = $eachfile;
	print "$File_input\n";
	$fi = $File_input;
	chop $fi;chop $fi;chop $fi;chop $fi;
	open (FO, ">$fi.unique_seq.fas") or die "no output file\n";
	open (FO2, ">$fi.duplicate_ids.txt") or die "no duplicates file\n";
	my $seqio_object = Bio::SeqIO->new(-file => "$File_input");
	my %unique_desc;
	my %unique_seq;
	#my %unique_seq2;

	while (my $seq = $seqio_object->next_seq) 
	{      
		my $current_name = $seq->display_id();
		my $desc = $seq->desc();
		my $len = $seq->length;
		my $sequence = $seq->seq;
		if ($len gt 0)
		{
			#print "$.\n";
			#print FO "$current_name\t$desc\t$len\n";
			if (defined $unique_desc{$sequence})
			{
				print FO2 "$unique_desc{$sequence}\t$current_name$desc\n";
			}
			if (not defined $unique_desc{$sequence})
			{
				$unique_desc{$sequence}="$current_name$desc";
			}
			$unique_seq{"$current_name$desc"}=$sequence;
		}
	}

	for $sequ (keys %unique_desc)
	{
		print FO ">$unique_desc{$sequ}\n$unique_seq{$unique_desc{$sequ}}\n";
	}
	undef %unique_desc;
	undef %unique_seq;
	close FO;
	close FO2;
#}