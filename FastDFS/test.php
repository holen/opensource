<?php
//所上传的文件
$filename = "aa.php";
//调用FastDFS类
$fdfs = new FastDFS();
//上传文件 $filename 是所上传的文件，html是上传后的更名后缀名为.html
$file_info = $fdfs->storage_upload_by_filename($filename,html);
//输出上传文件目录和文件名
echo $file_info['filename'];
?>
