<?php
mysql_connect("localhost","zenoss","zenoss");
mysql_select_db("smsd");

if(isset($_GET['id']) && isset($_GET['val'])){
	    $val = $_GET['val'] ? 0 : 1;
        if($_GET['type']){
			mysql_query("UPDATE support SET Oncall=$val WHERE UID=$_GET[id]") or die("An error ocured");
		}else{
			mysql_query("UPDATE support SET Switchover=$val WHERE UID=$_GET[id]");
        }
echo "check";
exit;
}

if(isset($_GET['id']) && isset($_GET['delete'])){
	$id = intval($_GET['id']);
	mysql_query("DELETE FROM support WHERE UID=$id LIMIT 1") or die(mysql_error());
	echo "check";
	exit;
}
if(isset($_POST['name']) && isset($_POST['number'])){
	if(mysql_query("INSERT INTO support ( Name,Number,Oncall,Switchover )
	VALUES ( '$_POST[name]', '$_POST[number]', '0', '0');")){
	header("location:oncall.php");
	exit;
	}else{
		exit("An error ocured.<br><br>".mysql_error());
	}
}

$result1 = mysql_query("SELECT * FROM support ORDER BY Name ASC");
$result2 = mysql_query("SELECT * FROM support ORDER BY Name ASC");

?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>

<script language="javascript" type="text/javascript">
<!-- 
oncall = Array();
switchover = Array();
autoset = true
<?php
while($jsdata = mysql_fetch_array($result2)){
	echo 'oncall['.$jsdata['UID'].']='.$jsdata['Oncall'].";\n";
	echo 'switchover['.$jsdata['UID'].']='.$jsdata['Switchover'].";\n";
	$idarray .= $jsdata['UID'].',';
}
$idarray = substr($idarray,0,strlen($idarray)-1);
echo "idarray = Array(".$idarray.")\n";
?>

function getAjaxObject(){
var a;try{a=new XMLHttpRequest();
}catch(e){try{
a=new ActiveXObject("Msxml2.XMLHTTP");
}catch(e){try{
a=new ActiveXObject("Microsoft.XMLHTTP");
}catch(e){alert("A cricitcal error occurred!\n--------\nYour browser does not support this web-aplication!\nFor more information, contact the webmaster or your dealer.\n\n Specific error message:\n\n"+e+"\n");
return false;
}}}return a;}

function randomiser() {
        var chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
        var string_length = 8;
        var randomstring = '';
        for (var i=0; i<string_length; i++) {
                var rnum = Math.floor(Math.random() * chars.length);
                randomstring += chars.substring(rnum,rnum+1);
        }
        return randomstring;
}

function checktrue(){
	if(autoset){
		for(x in switchover){
			if(switchover[x]){
				setfunc(x,1,0,1)
				break
			}
		}
	}
}

function setfunc(id,val,type,x,id2){
	ajaxRequest = getAjaxObject()
	ajaxRequest.onreadystatechange = function(){
	if(ajaxRequest.readyState == 4){
			if(ajaxRequest.responseText!='check'){
				alert(ajaxRequest.responseText)
			}else{
				if(type){
					oncall[id] = oncall[id] ? 0:1;
					document.getElementById('oncall'+id).innerHTML=oncall[id] ? 'Yes' : 'No';
					document.getElementById('row'+id).style.backgroundColor = oncall[id] ? '#FFFF66' : '';
				}else{
					switchover[id] = switchover[id] ? 0:1;
					document.getElementById('switchover'+id).innerHTML=switchover[id] ? 'Yes' :'No';
					if( autoset ){
						if(isNaN(x)){x=0;id2=id;}
						for(;x<idarray.length;x++){
							if(switchover[idarray[x]] && id2 != idarray[x] ){
								setfunc(idarray[x],1,0,x+1,id2)
								break;
							}
						}						
					}
				}                        
			}
		}
	}
	randomstring = randomiser();
	requestUrl = "oncall.php?id="+id+"&val="+val+"&type="+type+"&randomiser="+randomstring;
	ajaxRequest.open("GET",requestUrl, true);
	ajaxRequest.send(null); 
}




function del(id){
	precolor = document.getElementById('row'+id).style.backgroundColor
	document.getElementById('row'+id).style.backgroundColor = '#FFAAAA'
	if(!confirm('Are you sure you want to delete this user?')){
		document.getElementById('row'+id).style.backgroundColor = precolor;
		return false
	}
	ajaxRequest = getAjaxObject();
	ajaxRequest.onreadystatechange = function(){
		if(ajaxRequest.readyState == 4){
			if(ajaxRequest.responseText!='check'){
				alert(ajaxRequest.responseText);
			}else{
				delete switchover[id];
				delete autoset[id];
				document.getElementById("row"+id).style.display='none'
				alert('The user has been deleted.')
			}
		}
	}
	randomstring = randomiser();
   ajaxRequest.open("GET","oncall.php?id="+id+"&delete=true&randomiser="+randomstring, true);
   ajaxRequest.send(null); 
}

//-->
</script>
<style type="text/css">
body{
	background-image:url(background_blue.jpg);
	background-repeat:repeat-x;
}
</style>
<title>pagina 1</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>
<body>

<h1 align="center">Who is on call ? </h1>

<b>Click on the Yes/No fields to change the value</b>
<br>
<br>

<table width="100%" border="1" cellpadding="2" cellspacing="0" id="test" >
<tr>
			<td style="background-color:#33FFFF;"> <strong>Name</strong></td>
			<td style="background-color:#33FFFF;"> <strong>Number</strong> </td>
			<td style="background-color:#33FFFF;"> <strong>Oncall</strong></td>
			<td style="background-color:#33FFFF;"> <strong>Switchover: </strong> <br>  Multiple: <a style="cursor:pointer;" onClick="autoset = autoset ? 0:1; this.innerHTML = autoset ? '&nbsp;<u>Off</u>':'&nbsp;<u>On</u>';checktrue()" >&nbsp;<u>Off</u></a></td>
			<td style="background-color:#33FFFF;"> <strong>Action</strong></td>
</tr>

<?php

while($row = mysql_fetch_array($result1))
{
 echo "<tr ".($row['Oncall']?'style="background-color:#FFFF66;"':'')."id='row$row[UID]'>
        <td > $row[Name] </td>
        <td > $row[Number] </td>
        <td ><a style='cursor:pointer' id='oncall$row[UID]'
onclick='setfunc($row[UID],oncall[$row[UID]],1)'>".($row['Oncall']?'Yes':'No')."</a></td>
        <td ><a style='cursor:pointer' id='switchover$row[UID]'
onclick='setfunc($row[UID],switchover[$row[UID]],0)'>".($row['Switchover']?'Yes':'No')."</a></td>
		<td onmouseover=\"this.style.backgroundColor='#FFAAAA'\" onmouseout=\"this.style.backgroundColor=''\" > <a style='cursor:pointer' onclick='del($row[UID])'> Delete <a/> </td>
        </tr>";
}


?>
</table>

<form method="post" action="oncall.php">
<table width="600">
<tr>
  <td colspan="2"><strong>Add a user </strong></td>
  </tr>
<tr>
  <td width="92">Name</td>
  <td width="496"><input type="text" name="name"></td>
</tr>
<tr>
  <td>Number</td>
  <td><input type="text" name="number"></td>
</tr>
<tr>
<td height="26"><input type="submit" name="Submit" value="Execute"></td>
<td>&nbsp;</td>
</tr>
</table>
</form>
<br>
<br>


</body>
</html>
