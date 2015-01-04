<%inherit file="base.mako"/>

<%def name="title()">
SMS Vault - SMS Backup Manager
</%def>

<%def name="header()">
  ${self.main_menu()}
</%def>
  
  <div class="row" >
    <div class="panel panel-default col-md-6 col-lg-4 hidden-sm hidden-xs">
      <div class="panel-body">
        <div class="input-group">
          <input type="text" class="form-control" placeholder="Search ...">
          <span class="input-group-btn">
            <button class="btn btn-primary" type="button">Search</button>
          </span>
        </div>
        
      </div>
      
      <div  style="overflow-y: auto; height: 500px;">
      <ul class="nav nav-pills nav-stacked">
        <!--<li role="presentation" class="active"><a href="#">Home</a></li>-->
        %for contact in contact_names:
          <li role="presentation">
            <a href="javascript:">${contact}
              
              <span class="badge">
                <span class="glyphicon glyphicon-resize-small" aria-hidden="true"></span>
                ${msg_counts[contact]['incoming']+msg_counts[contact]['outgoing']}
              </span>
              <span class="badge">
                <span class="glyphicon glyphicon-log-in" aria-hidden="true"></span>
                ${msg_counts[contact]['incoming']}
              </span>
              
              <span class="badge">
                <span class="glyphicon glyphicon-new-window" aria-hidden="true"></span>
                ${msg_counts[contact]['outgoing']}
              </span>
            </a>
          </li>
        %endfor
      </ul>
      </div>
    </div>
  </div>  
