<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <meta http-equiv="Content-Type" content="text/html, charset=utf-8">
  <title>PHP 测试</title>
  <script language="javascript">
    function mycheck1(){
        if(myform.user.value==""){
            alter("姓名不能为空!");
            //myform.user.focus();
            //return false;
        }
        if(myform.pwd.value==""){
            alter("密码不能为空!");
            //myform.pwd.focus();
            //return false;
        }
    }
    </script>
 </head>
 <body>
 <form action="" method="post" name="myform">
   <table width="405" border="1" cellpadding="1" cellspacing="1" bordercolor="#FFFFFF" bgcolor="#999999">
      <tr bgcolor="#FFCC33">
        <td width="103" height="25" align="right">姓名: </td>
        <td width="144" height="25"><input name="user" type="text" id="user" size="20" maxlength="100"></td>
      </tr>
      <tr bgcolor="#FFCC33">
        <td width="103" height="25" align="right">密码: </td>
        <td width="289" height="25" colspan="2"><input name="pwd" type="password" id="pwd" size="20" maxlength="100"></td>
      </tr>
      <tr align="center" bgcolor="#FFCC33">
        <td height="25" colspan="3"><input type="submit" name="submit" onclick="mycheck1()" value="提交">
            <input type="reset" name="submit2" value="重置"></td>
      </tr>
    </table>
  </form>
  </body>
</html>
