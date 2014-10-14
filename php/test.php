<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <meta http-equiv="Content-Type" content="text/html, charset=utf-8">
  <title>PHP 测试</title>
 </head>
 <body>
 <table>
 <?php
 echo "当前文件路径：".__FILE__;
 echo "<br>当前行数：".__LINE__;
 echo "<br>当前PHP版本信息：".PHP_VERSION;
 echo "<br>当前操作系统：".PHP_OS;
 echo "<br>IP地址: ".$_SERVER['SERVER_ADDR'];
 echo "<br>Cookie: ".$_COOKIE;
 $change_name = "trans";
 $trans = "You can see me!";
 echo "<br>";
 echo $change_name;
 echo "<br>";
 echo $$change_name;
 $a = 100;
 $b = 200;
 echo "<br>";
 echo "\$a + \$b = ".($a + $b);
 echo "<br>";
 $arr=array(0=>'php', 1=>'is', 'the'=>'the', 'str'=>'best');
 print_r($arr);
 echo "<br>";
 $str="PHP is@ best@ wahaha";
 $str_arr=explode("@",$str);
 print_r($str_arr);
 $array=implode("*",$str_arr);
 echo "<br>";
 echo $array;
 echo "<br>";
 echo $arr[0]." ".$arr['the'];
 echo "<br>";
 foreach ($arr as $key=>$value){
     echo $key." ".$value;
     echo "<br>";
     }
 if (!$boo):
     echo "not exits";
 else:
     echo "exits";
 endif;
 echo "<br>";
 function example($num){
     return "$num * $num = ".$num * $num;
    }
 echo example(10);
 function come($name = "jack") {
     echo "<br>";
     echo "$name 走了";
 }
 $func = "come";
 $func();
 $func("Tom");
 /*
 function &example(){
     return "111";
 }
 $a = &example();
 echo $a;
  */
 ?>
 </table>
 <form action="test.php" method="post" name="form1" enctype="multipart/form-data">
   <table width="405" border="1" cellpadding="1" cellspacing="1" bordercolor="#FFFFFF" bgcolor="#999999">
      <tr bgcolor="#FFCC33">
        <td width="103" height="25" align="right">姓名: </td>
        <td width="144" height="25"><input name="user" type="text" id="user" size="20" maxlength="100"></td>
      </tr>
      <tr bgcolor="#FFCC33">
        <td height="25" align="right">性别: </td>
        <td width="25" colspan="2" align="left"><input name="sex" type="radio" value="男" checked>男
          <input type="radio" name="sex" value="女">女</td>
      </tr>
      <tr bgcolor="#FFCC33">
        <td width="103" height="25" align="right">密码: </td>
        <td width="289" height="25" colspan="2"><input name="pwd" type="password" id="pwd" size="20" maxlength="100"></td>
      </tr>
      <tr bgcolor="#FFCC33">
        <td height="25" align="right">学历: </td>
        <td height="25" colspan="2" align="left"><select name="select">
            <option value="专科">专科</option>
            <option value="本科">本科</option>
          </select></td>  
      </tr>
      <tr bgcolor="#FFCC33">
        <td height="25" align="right">爱好: </td>
        <td height="25" colspan="2" align="left">
          <input type="checkbox" name="fond[]" id="fond[]" value="音乐">音乐
          <input type="checkbox" name="fond[]" id="fond[]" value="其他">其他
        </td>
      </tr>
      <tr bgcolor="#FFCC33">
        <td height="25" align="right">个人简介: </td>
        <td height="25" colspan="2"><textarea name="intro" cols="28" rows="4" id="intro"></textarea></td>
      </tr>
      <tr align="center" bgcolor="#FFCC33">
        <td height="25" colspan="3"><input type="submit" name="submit" value="提交">
            <input type="reset" name="submit2" value="重置"></td>
      </tr>
    </table>
  </form>
  <!-- 在<form>标记外添加 php 脚本 -->
 <script language="javascript">
    document.write("您的浏览器支持JavaScript脚本");
    document.write("<br>");
 </script>
 <noscript>
    您的浏览器不支持JavaScript脚本
    document.write("<br>");
 </noscript>
 <script language="javascript">
 function mycheck(){
    if(form1.user.value==""){
        alter("姓名不能为空!");
        form1.user.focus();
        return false;
    }
    if(form1.pwd.value==""){
        alter("密码不能为空!");
        form1.pwd.focus();
        return false;
    }
 }
 </script>
  <?php 
 if($_POST[submit]!=""){
     echo "您的个人简历内容是：";
     echo "<br>";
     echo "姓名：".$_POST[user];
     echo "<br>";
     echo "性别：".$_POST[sex];
     echo "<br>";
     echo "密码：".$_POST[pwd];
     echo "<br>";
     echo "学历：".$_POST[select];
     echo "<br>";
     echo "爱好：";
     for($i=0;$i<count($_POST[fond]);$i++)
        echo $_POST[fond][$i]."&nbsp;&nbsp;";
     echo "<br>";
     echo "个人简介：".$_POST[intro];
 } 
?>
  </body>
<!-- 在<body>标记外，添加JavaScript脚本-->
<!-- JavaScript 脚本通常写在<head>...</head>标记和<body>...</body>标记之间。写在<head>标记中间的一般是函数和时间处理函数；
    写在<body>标记中间的是网页内容或调用函数的程序快。-->
</html>
