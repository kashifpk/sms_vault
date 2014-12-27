<%inherit file="base.mako"/>

<%def name="title()">
SMS Valut - Import Messages
</%def>

<%def name="extra_head()">
## extra_head should be defined in project's base.mako

<link rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/dojo/1.10.1/dojox/form/resources/UploaderFileList.css" type="text/css" charset="utf-8" />

</%def>

<h1>Import Messages</h1>
<br />
<form action="${request.route_url('import_smses')}" enctype="multipart/form-data" method="POST">
    <label for="uploader">Select message backup files to import</label>
    <input type="file" id="uploader" name="uploader" multiple="true" data-dojo-type="dojox/form/Uploader"
    data-dojo-props="label: 'Select files to import', uploadOnSelect: false" />
    <div id="files" data-dojo-type="dojox/form/uploader/FileList" data-dojo-props="uploaderId: 'uploader'"></div>
    <br />
    

    <button type="submit" class="btn btn-primary">Import</button>
</form>
