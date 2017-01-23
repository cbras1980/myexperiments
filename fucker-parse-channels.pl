use LWP::UserAgent;
use HTTP::Cookies;
use JSON;
use Test::JSON;
use utf8;

binmode STDOUT, ":utf8";

my $mac = $ARGV[0];

my $targethost = "tech.stmteam.org";

#Replace a string without using RegExp.
sub str_replace {
	my $replace_this = shift;
	my $with_this  = shift; 
	my $string   = shift;
	
	my $length = length($string);
	my $target = length($replace_this);
	
	for(my $i=0; $i<$length - $target + 1; $i++) {
		if(substr($string,$i,$target) eq $replace_this) {
			$string = substr($string,0,$i) . $with_this . substr($string,$i+$target);
			return $string; #Comment this if you what a global replace
		}
	}
	return $string;
}

#my $filemac = str_replace('%3A','',$mac);
my $filemac = $mac;
$filemac =~ s/%3A//g;

my $json;

my $cookie = "mac=$mac; stb_lang=ru; timezone=Europe%2FKiev";
#print "Checking mac: $cookie\n";
 
my $ua = LWP::UserAgent->new;
 
my $server_endpoint = "http://$targethost:8000/portal.php?type=stb&action=handshake&token=&JsHttpRequest=1-xml";
#my $server_endpoint2 = "http://$targethost:8000/portal.php?type=itv&action=get_all_channels&JsHttpRequest=1-xml";
my $server_endpoint2 = "http://$targethost:8000//portal.php?type=itv&action=get_ordered_list&genre=48&fav=0&sortby=number&hd=0&p=0&JsHttpRequest=1%2Dxml&";

my $req = HTTP::Request->new(GET => $server_endpoint);
my $req2 = HTTP::Request->new(GET => $server_endpoint2);

$req->header( 'Host' => '$targethost:8000' );
$req->header( 'Connection' => 'keep-alive' );
$req->header( 'Referer' => 'http://$targethost:8000/c/' );
$req->header( 'X-User-Agent' => 'Model: MAG250; Link: Ethernet,WiFi' );
$req->header( 'X-Requested-With' => 'com.vasilchmax' );
$req->header( 'User-Agent' => 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 234 Safari/533.3' );
$req->header( 'Accept-Encoding' => 'gzip,deflate' );
$req->header( 'Accept-Language' => 'en-US' );
$req->header( 'Accept-Charset' => 'utf-8, iso-8859-1, utf-16, *;q=0.7' );
$req->header( 'Cookie' => $cookie );
 
my $resp = $ua->request($req);
if ($resp->is_success) {
    my $message = $resp->decoded_content;
    $json = $resp->decoded_content;
    my $data = decode_json($json);
    my $token = $data->{'js'}->{'token'};
}
else {
    print "HTTP GET error code: ", $resp->code, "\n";
    print "HTTP GET error message: ", $resp->message, "\n";
}

$req2->header( 'Host' => '$targethost:8000' );
$req2->header( 'Connection' => 'keep-alive' );
$req2->header( 'Referer' => 'http://$targethost:8000/c/' );
$req2->header( 'X-User-Agent' => 'Model: MAG250; Link: Ethernet,WiFi' );
$req2->header( 'X-Requested-With' => 'com.vasilchmax' );
$req2->header( 'User-Agent' => 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 234 Safari/533.3' );
$req2->header( 'Accept-Encoding' => 'gzip,deflate' );
$req2->header( 'Accept-Language' => 'en-US' );
$req2->header( 'Accept-Charset' => 'utf-8, iso-8859-1, utf-16, *;q=0.7' );
$req2->header( 'Cookie' => $cookie );
$req2->header( 'Authorization' => 'Bearer '.$token );

$resp = $ua->request($req2);
open(my $fh2, '>', 'channels.json') or die "Not able to open file";
if ($resp->is_success) {
    my $message = $resp->decoded_content;
    print $fh2 $message;
    $json = $resp->decoded_content;
    eval {    
        my $arquivo = $filemac.'-channels.txt';

        open(my $fh, '>', $arquivo) or die "Not able to open file";

        my $data = decode_json($json); 
        my $alldata = $data->{'js'}->{'data'};
        my @array=keys($alldata);
        my $size=$#array;
        
        print $fh "#EXTM3U\n";

        while ( my( $key, $value ) = each $alldata ) {
            my $id = $value->{'id'};
            my $name = $value->{'name'};
            my $nameurl = $value->{'name'};
            my $stream = $value->{'cmd'};
            my $logo = $value->{'logo'};
            $stream =~ s/auto //;
            $nameurl =~ s/ /%20/g;
            print $fh "#EXTINF:-1 tvg-name=\"".$name."\" audio-track=\"pt\" tvg-logo=\"$logo".$nameurl.".png\" group-title=\"PORTUGAL\", ".$name."\n";
            print $fh "".$stream."\n";
        }
        #print $fh $mac."\n";
        #print $fh "".$alldata->{'cmd'}."\n";
        print "".$alldata->{'cmd'}."\n";
        close($fh);
    } or do {
        #my $e = $@;
        #print "NOT VALID MAC\n";
    }
}
else {
    print "HTTP GET error code: ", $resp->code, "\n";
    print "HTTP GET error message: ", $resp->message, "\n";
}

close($fh2);
