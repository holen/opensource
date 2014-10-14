<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    </head>
    <?php echo "Hello world ! " ?>
    <body>
        <table>
        <?php for($i=1;$i<=4;$i++){?>
            <tr>
                <?php for($j=0;$j<3;$j++){?>
                <td><?php echo $i;?></td>
                <?php }?>
            </tr>
        <?php }?>    
        </table>
    </body>
</html>
