<!DOCTYPE html>
<html>
<head>
    <title>My Web Page</title>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script>
        $(document).ready(function(){
            $('#all').click(function(){
                if(this.checked){
                    $(':checkbox').each(function(){
                        this.checked = true;
                    });
                } else {
                    $(':checkbox').each(function(){
                        this.checked = false;
                    });
                }
            });
        });
    </script>
</head>
<body>
    <form method="POST">
        <label for="textfield">輸入關鍵字:</label><br>
        <input type="text" id="textfield" name="textfield"><br>
        <label>勾選選單:</label><br>
        <input type="checkbox" id="all" name="checkbox" value="全選">
        <label for="all">全選</label><br>
        <input type="checkbox" id="china" name="checkbox" value="中國">
        <label for="china">中國</label><br>
        <input type="checkbox" id="usa" name="checkbox" value="美國">
        <label for="usa">美國</label><br>
        <input type="checkbox" id="germany" name="checkbox" value="德國">
        <label for="germany">德國</label><br>
        <input type="checkbox" id="uk" name="checkbox" value="英國">
        <label for="uk">英國</label><br>
        <input type="submit" value="開始">
    </form>
</body>
</html>
