<tal:block metal:use-macro="here/templates/macros/page2">
<tal:block metal:fill-slot="contentPane">

<form method=post id="pred_thresh_form"
    tal:attributes="action string:${here/absolute_url_path}">
    <input type="hidden" name="zenScreenName"
        tal:attributes="value template/id" />


        <tal:block tal:define="message request/message | string:State at time:; 
            tabletitle string:${message} ${here/getNowString}">
        <tal:block metal:use-macro="here/zenuimacros/macros/zentable">

        <!--====Optional titlebar slots=============

            <tal:block metal:fill-slot="filterslot">
            </tal:block>

            <tal:block metal:fill-slot="menuslot">
            </tal:block>

            ==========================================-->

        <tal:block metal:fill-slot="zentablecontents">
        <!-- BEGIN TABLE CONTENTS -->

    <tr>
        <td class="tableheader">Name</td>
        <td class="tablevalues" tal:content="here/id"/>
    </tr>
    <tr>
        <td class="tableheader">Data Point</td>
        <td class="tablevalues" tal:condition="here/isManager">
            <select class="tablevalues" name="dsnames:list"
                tal:define="curdses here/dsnames">
                <option tal:repeat="ds here/getRRDDataPointNames"
                    tal:attributes="value ds; selected python:ds in curdses"
                    tal:content="ds">ifInOctets</option>
            </select>
        </td>
        <td class="tablevalues" tal:condition="not:here/isManager"
            tal:content="python:', '.join(here.dsnames)"/>
    </tr>
    <tr>
        <td class="tableheader">Alpha</td>
        <td class="tablevalues" tal:condition="here/isManager">
        <input class="tablevalues" type="text" name="alpha" size="50"
            tal:attributes="value here/alpha" />
        </td>
      <td class="tablevalues" tal:condition="not:here/isManager" 
            tal:content="here/alpha"/>
    </tr>
    <tr>
        <td class="tableheader">Beta</td>
        <td class="tablevalues" tal:condition="here/isManager">
        <input class="tablevalues" type="text" name="beta" size="50"
            tal:attributes="value here/beta" />
        </td>
      <td class="tablevalues" tal:condition="not:here/isManager" 
            tal:content="here/beta"/>
    </tr>
    <tr>
        <td class="tableheader">Gamma</td>
        <td class="tablevalues" tal:condition="here/isManager">
        <input class="tablevalues" type="text" name="gamma" size="50"
            tal:attributes="value here/gamma" />
        </td>
      <td class="tablevalues" tal:condition="not:here/isManager" 
            tal:content="here/gamma"/>
    </tr>
    <tr>
        <td class="tableheader">Rows</td>
        <td class="tablevalues" tal:condition="here/isManager">
        <input class="tablevalues" type="text" name="rows" size="50"
            tal:attributes="value here/rows" />
        </td>
      <td class="tablevalues" tal:condition="not:here/isManager" 
            tal:content="here/rows"/>
    </tr>
    <tr>
        <td class="tableheader">Season</td>
        <td class="tablevalues" tal:condition="here/isManager">
        <input class="tablevalues" type="text" name="season" size="50"
            tal:attributes="value here/season" />
        </td>
      <td class="tablevalues" tal:condition="not:here/isManager" 
            tal:content="here/season"/>
    </tr>
    <tr>
        <td class="tableheader">Window</td>
        <td class="tablevalues" tal:condition="here/isManager">
        <input class="tablevalues" type="text" name="window" size="50"
            tal:attributes="value here/window" />
        </td>
      <td class="tablevalues" tal:condition="not:here/isManager" 
            tal:content="here/window"/>
    </tr>
    <tr>
        <td class="tableheader">Threshold</td>
        <td class="tablevalues" tal:condition="here/isManager">
        <input class="tablevalues" type="text" name="threshold" size="50"
            tal:attributes="value here/threshold" />
        </td>
      <td class="tablevalues" tal:condition="not:here/isManager" 
            tal:content="here/threshold"/>
    </tr>
    <tr>
        <td class="tableheader">Delta</td>
        <td class="tablevalues" tal:condition="here/isManager">
        <input class="tablevalues" type="text" name="delta" size="50"
            tal:attributes="value here/delta" />
        </td>
      <td class="tablevalues" tal:condition="not:here/isManager" 
            tal:content="here/delta"/>
    </tr>
    <tr>
        <td class="tableheader">Prediction Color</td>
        <td class="tablevalues" tal:condition="here/isManager">
        <input class="tablevalues" type="text" name="predcolor" size="50"
            tal:attributes="value here/predcolor" />
        </td>
      <td class="tablevalues" tal:condition="not:here/isManager" 
            tal:content="here/predcolor"/>
    </tr>
    <tr>
        <td class="tableheader">Confidence Band Color</td>
        <td class="tablevalues" tal:condition="here/isManager">
        <input class="tablevalues" type="text" name="cbcolor" size="50"
            tal:attributes="value here/cbcolor" />
        </td>
      <td class="tablevalues" tal:condition="not:here/isManager"
            tal:content="here/cbcolor"/>
    </tr>
    <tr>
        <td class="tableheader">Tick Color</td>
        <td class="tablevalues" tal:condition="here/isManager">
        <input class="tablevalues" type="text" name="tkcolor" size="50"
            tal:attributes="value here/tkcolor" />
        </td>
      <td class="tablevalues" tal:condition="not:here/isManager" 
            tal:content="here/tkcolor"/>
    </tr>
    <tr>
        <td class="tableheader">Event Class</td>
        <td class="tablevalues" tal:condition="here/isManager">
        <select class="tablevalues" name="eventClass">
            <option tal:repeat="evtcls here/getEventClassNames" 
                    tal:content="evtcls" 
                    tal:attributes="selected python:evtcls==here.eventClass"/>
        </select>
        <!--
        <input class="tablevalues" type="text" name="eventClass" size="50"
            tal:attributes="value here/eventClass" />
        -->
        </td>
    </tr>
    <tr>
        <td class="tableheader">Severity</td>
        <td class="tablevalues" tal:condition="here/isManager">
        <select class="tablevalues" name="severity:int">
           <option tal:repeat="sev here/ZenEventManager/getSeverities"
                   tal:content="python:sev[0]"
                   tal:attributes="selected python:sev[1]==here.severity; value python:sev[1]"/>
        </select>
        </td>
    </tr>
    <tr>
        <td class="tableheader">Escalate Count</td>
        <td class="tablevalues" tal:condition="here/isManager">
        <input class="tablevalues" type="text" 
            name="escalateCount:int" size="10"
            tal:attributes="value here/escalateCount" />
        </td>
        <td class="tablevalues" tal:condition="not:here/isManager" 
            tal:content="here/escalateCount"/>
    </tr>
    <tr>
        <td class="tableheader">Enabled</td>
        <td class="tablevalues" tal:condition="here/isManager">
        <select class="tablevalues" name="enabled:boolean">
            <option tal:repeat="e python:(True,False)" tal:content="e"
                    tal:attributes="value e; selected python:e==here.enabled"/>
        </select>
        </td>
        <td class="tablevalues" tal:condition="not:here/isManager" 
            tal:content="here/enabled"/>
    </tr>
    <tr>
        <td class="tableheader">
        </td>
        <td class="tableheader" colspan="3">
            <input class="tableheader" type="submit" value=" Save "
                name="zmanage_editProperties:method" />
        </td>
    </tr>

        <!-- END TABLE CONTENTS -->

        </tal:block>
        </tal:block>
        </tal:block>

</form>

<script>
var pred_thresh_form = new Zenoss.dialog.DialogFormPanel ( {
	existingFormId:	'pred_thresh_form',
	jsonResult: false
} );
</script>

</tal:block>
</tal:block>
