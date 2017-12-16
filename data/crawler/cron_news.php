#!/usr/bin/php -q

<?php


echo "\nstock cron start".date("Ymd")."\n"; 




$start=1;
$display=20;
$total=20;
$newname = "news.txt";
$line = "";

for($start=1;$start <=$total; $start=$start+$display)
{


	$encText = urlencode("insert search keyword here");
	$url = "https://openapi.naver.com/v1/search/news.json?display=$display&start=$start&sort=date&query=".$encText;


	if($debug) echo " url:".$url;
	$response =  getSearchResult($url);
	if($debug) echo " result:".$response;

	if ($response !== false) 
	{
		$rs = getJsonArray($response);
		if($debug) print_r($rs);
		for($i=0; $i < sizeof($rs['items']); $i++)
		{
			$item = $rs['items'][$i]; 
			$title = $item['title'];

			$title = getNewHighlightTag($title);
			$desc = getNewHighlightTag($desc);
			$originallink = getNewHighlightTag($originallink);


			$desc = trim(str_replace("\n", " ", $item['description']));
			$desc = str_replace("\t", " ", $desc);
			$pubDate = $item['pubDate'];
			$link = $item['link'];

			$line .= $pubDate."\t".$title."\t".$desc."\t".$originallink."\n"; 
		}
			
	}	
	else {
		echo "Error: It's not possible to get $new_request_addr";
	}
}
echo "\nline:".$line;
file_put_contents($newname, $line, FILE_APPEND);
$total_request++;
}
}



function getNewHighlightTag($title)
{
	$title = str_replace("&lt;b&gt;", "<strong class=\"hl\">", $title);
	$title = str_replace("<b>", "<strong class=\"hl\">", $title);
        $title = str_replace("&lt;/b&gt;", "</strong>", $title);
        $title = str_replace("</b>", "</strong>", $title);
	$title = str_replace("&", "&amp;", $title);

	return $title;
}

function getJsonArray($response)
{
	$json_array = json_decode($response, true);

	switch(json_last_error())
	{
		case JSON_ERROR_DEPTH:
		    echo ' - Maximum stack depth exceeded';
		break;
		case JSON_ERROR_CTRL_CHAR:
		    echo ' - Unexpected control character found';
		break;
		case JSON_ERROR_SYNTAX:
		    echo ' - Syntax error, malformed JSON';
		break;
		case JSON_ERROR_NONE:
		    //echo ' - No errors';
		break;
	}
	return $json_array; 

}

function getSearchResult($url)
{
	$client_id = "insert your id here";
	$client_secret = "insert your screte code here";
	$is_post = false;


	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_POST, $is_post);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	$headers = array();
	$headers[] = "X-Naver-Client-Id: ".$client_id;
	$headers[] = "X-Naver-Client-Secret: ".$client_secret;
	curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
	$response = curl_exec ($ch);
	$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
	//echo "status_code:".$status_code;
	curl_close ($ch);
	if($status_code == 200) {
		return $response;
	} else {
		echo "Error 내용:".$response;
		return false;
	}


}

?>


