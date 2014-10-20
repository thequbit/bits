<!doctype html>
<!--[if IE 9]><html class="lt-ie10" lang="en" > <![endif]-->
<html>
<head>

    <title>bits - Requirements and Ticketing System</title>

    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
   
    <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'> 
    <link rel="stylesheet" href="static/foundation/css/foundation.css" />
    
    <style>

        a.extra-small-button {
            /*padding: 0.875rem 1.00rem 0.9375rem !important;*/
            
        }

        /*
        div.row {
            max-width: 70.0rem;
        }
        */

        div.task-title {
            color: rgba(0,255,0,0.8);
            display: inline-block;
        }

        div.ticket-title {
            color: rgba(255,0,0,0.8);
            display: inline-block;
        }

        div.list-title {
            color: rgba(0,0,255,0.8);
            display: inline-block;
        }

        div.requirement-title {
            color: rgba(64,64,128,0.8);
            display: inline-block;
        }

        div.milestone-title {
            color: rgba(64,128,64,0.8);
            display: inline-block;
        }

        div.note-title {
            color: rgba(128,64,64,0.8);
            display: inline-block;
        }

        div.top-links a {
            #margin-left: 10px;
            margin-left: 10px !important;
        }

        aside.side-menu {
            border-left: 1px solid #DDD;
        }

        textarea {
            min-height: 150px;
        }

        div.padded-bottom {
            padding-bottom: 6px;
        }

        div.shadow {
             box-shadow: 0px 0px 0px 1px #DDD, 0px 4px 8px rgba(221, 221, 221, 0.9);
        }

        div.error-box {
            color: red;
            font-weight: bold;
        }

        div.markdown-text {
            padding-top: 8px; padding-right: 2px;
        }

        div.top-border {
            padding-top: 3px;
            border-top: 1px solid #DDD;
        }

        div.bottom-border {
            padding-bottom: 6px;
            border-bottom: 1px solid #DDD;
        }

        div.left-border {
            padding-left: 3px;
            border-left: 1px solid #DDD;
        }

        div.right-border {
            padding-right: 3px;
            border-right: 1px solid #DDD;
        }

        div.light-text {
            color: #DDD;
        }

        div.small-light-text {
            font-size: 80%;
            color: #BBB;
        }

        div.extra-small-light-text {
            font-size: 60%;
            color: #BBB;
        }

        div.list-container {
            min-height: 342px;
        }

        div.box {
            margin-top: 20px;
            padding: 5px;
            /*border: 1px solid #DDD;*/
            #border-radius: 4px;
        }

        div.box-title {
            margin-bottom: 8px;
            border-bottom: 1px solid #DDD;
            #border-top-left-radius: 4px;
            #border-rop-right-radius: 4px;
            padding-bottom: 2px;
        }

        div.box-inner-container {
            border-bottom: 1px solid #DDD;
            margin-bottom: 10px;
            margin-left: 20px;
            margin-right: 20px;
            padding-bottom: 10px;
        }

        div.container-inner {
            padding: 10px;
        }

        div.container-inner p {
            margin-bottom: 0px !important;
        }

        div.short-line-height {
            line-height: 100% !important;
        }

        div.box-small-text {
            font-size: 80%;
        }

        div.box-small-text b {
            padding-right: 5px;
        }



        div.block-container {
            border: 1px solid #DDD;
            border-radius: 2px;
        }

        /*
        div.block-title {
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            padding-left: 10px;
            background-color: #DDD;
            color: #333;
            border-bottom: 1px solid #DDD;
        }
        */

        div.block-contents {
            padding: 10px;
        }

        div.block-contents-inner {
            margin-top: 5px;
            padding: 5px;
            border: 1px solid #F9F9F9;
        }
        
        div.block-type {
            color: white;
            margin-top: 5px;
            margin-bottom: 10px;
            padding-left: 6px;
            padding-top: 2px;
            padding-bottom: 2px;
            padding-right: 6px;
            border-radius: 8px;
            display: inline-block;
        }

        div.block-type a {
            color: white !important;
        }

        div.indent {
            padding-left: 20px;
        }  
 
        div.indent-right {
            padding-right: 20px;
        }
 
        div.title-bar {
            width: 100%;
            border-bottom: 1px solid #DDD;
            margin-bottom: 10px;
            background-color: #EEE;
        }

        div.title-bar h3 {
            margin-bottom: 0.15rem !important;
        }


    </style>



</head>
<body>

    % if token == None or user == None:

        <script>
            window.location.href = "/login";
        </script>

    % else:

    <div class="title-bar"> 
        <div class="row">
            <div class="large-12 columns">
                <!--<div class="right" style="padding-top: 10px;">
                    <a href="/logout">Logout</a>
                </div>-->
                <h3>bits</h3>
            </div>
        </div>
    </div>

    <script src="static/foundation/js/vendor/jquery.js"></script>
    <script src="static/foundation/js/foundation.min.js"></script>
    <script src="static/foundation/js/vendor/modernizr.js"></script>

    <script>
        $(document).foundation();
    </script>
    
    <div class="row">
         <div class="large-12 columns">
            ${self.body()}
        </div>
    </div>
    
    % endif
    

</body>
</html>
