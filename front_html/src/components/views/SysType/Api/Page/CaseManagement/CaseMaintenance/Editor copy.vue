<template>
    <div>
        <template>
            <el-drawer
            :title="dialogTitle"
            size="1400px"
            :wrapperClosable="false"
            :visible.sync="dialogVisible"
            direction='rtl'
            :before-close="dialogClose">
                <el-steps :active="StepsRomeData.active" simple :process-status="StepsRomeData.processStatus" finish-status="success">
                    <el-step title="维护基本信息"></el-step>
                    <el-step title="组合测试集"></el-step>
                    <el-step title="编写测试用例"></el-step>
                    <el-step title="效验用例参数"></el-step>
                </el-steps>
                <el-card style="height:755px"
                    v-loading="loading"
                    element-loading-text="拼命加载中"
                    element-loading-spinner="el-icon-loading">
                    <template v-if="StepsRomeData.active==0">
                        <div class="table">
                           <div class="father" style="width: 100%; height: 600px;">
                                <div class="son" style="width: 950px; height: 150px;">
                                    <el-card style="width:1000px" shadow="never">
                                        <el-form ref="BasicRomeData" :inline="true" :rules="BasicRomeData.rules" :model="BasicRomeData"  label-width="100px">
                                            <el-form-item prop="pageId" label="所属页面:">
                                                <el-select v-model="BasicRomeData.pageId" clearable placeholder="请选择" style="width:200px;float:left;" @click.native="GetPageNameOption()">
                                                    <el-option
                                                        v-for="item in BasicRomeData.pageNameOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item prop="funId" label="所属功能:">
                                                <el-select v-model="BasicRomeData.funId" clearable placeholder="请选择" style="width:200px;float:left;" @click.native="GetFunNameOption()">
                                                    <el-option
                                                        v-for="item in BasicRomeData.funNameOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item prop="environmentId" label="页面环境:">
                                                <el-select v-model="BasicRomeData.environmentId" clearable placeholder="请选择" style="width:200px;float:left;" @click.native="GetPageEnvironmentNameOption()">
                                                    <el-option
                                                        v-for="item in BasicRomeData.environmentNameOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item prop="testType" label="测试类型:">
                                                <el-select v-model="BasicRomeData.testType" clearable placeholder="请选择" style="width:200px;float:left;">
                                                    <el-option
                                                        v-for="item in BasicRomeData.testTypeOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item prop="labelId" label="用例标签:">
                                                <el-select v-model="BasicRomeData.labelId" clearable placeholder="请选择" style="width:200px;float:left;">
                                                    <el-option
                                                        v-for="item in BasicRomeData.labelNameOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item prop="priorityId" label="优先级:">
                                                <el-select v-model="BasicRomeData.priorityId" clearable placeholder="请选择" style="width:200px;float:left;">
                                                    <el-option
                                                        v-for="item in BasicRomeData.priorityNameOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                        <span style="float: left">{{ item.label }}</span>
                                                        <span style="float: right; color: #8492a6; font-size: 13px">{{ item.details }}</span>
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                            <el-form-item prop="caseName" label="用例名称:">
                                                <el-input v-model.trim="BasicRomeData.caseName" style="width:510px;"></el-input>
                                            </el-form-item>
                                            <el-form-item prop="caseState" label="用例状态:">
                                                <el-select v-model="BasicRomeData.caseState" clearable placeholder="请选择" style="width:200px;float:left;">
                                                    <el-option
                                                        v-for="item in BasicRomeData.caseStateOption"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                    </el-option>
                                                </el-select>
                                            </el-form-item>
                                        </el-form>
                                    </el-card>
                                </div>
                            </div>
                        </div>
                    </template>
                    <template v-else-if="StepsRomeData.active==1">
                        <div style="width:1261px;margin-left:100px">
                            <el-table
                                id="TestSet" 
                                row-key="id"
                                :data="TestSetRomeData.tableData"
                                height="710px"
                                border>
                                <el-table-column
                                    label="序列"
                                    align= "center"
                                    type="index"
                                    width="80">
                                </el-table-column>
                                <el-table-column
                                    label="接口名称"
                                    align= "center"
                                    width="500px"
                                    prop="apiName">
                                </el-table-column>
                                <el-table-column
                                    label="测试名称"
                                    align= "center"
                                    width="300px">
                                    <template slot-scope="scope">
                                        <el-input v-model="scope.row.testName" maxlength="10" clearable show-word-limit placeholder="例:异常的登录"></el-input>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    label="是否同步"
                                    align= "center"
                                    width="90px">
                                    <template slot-scope="scope">
                                    <el-switch v-model="scope.row.is_synchronous" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                        <el-tooltip placement="right">
                                            <div slot="content">此为单向同步,开启后只会同步:URL,请求的入参,不会同步参数值!<br/>开启时:在接口维护中修改此接口入参时,此接口在被用例运行时会以接口维护中的 <b>入参</b> 为准!<br/>关闭时:双向参数信息为独立!</div>
                                            <i class='el-icon-info'></i>
                                        </el-tooltip>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    label="接口状态"
                                    width="100px"
                                    align= "center">
                                    <template slot-scope="scope">
                                        <el-tag type="warning" v-if="scope.row.apiState=='InDev'" >研发中</el-tag>
                                        <el-tag type="success" v-else-if="scope.row.apiState=='Completed'" >已完成</el-tag>
                                        <el-tag type="info" v-else>弃用</el-tag>
                                    </template>
                                </el-table-column>   
                                <el-table-column
                                    label="启用"
                                    align= "center"
                                    width="90px">
                                    <template slot-scope="scope">
                                    <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                    align="center"
                                    width="100px">
                                    <template slot="header">
                                        <el-button type="primary" @click="OpenApiMainDialog()">新增</el-button>
                                    </template>
                                    <template slot-scope="scope" style="width:100px">
                                        <el-button
                                            size="mini"
                                            type="danger"
                                            @click="handleDelete(scope.$index, scope.row)">移除
                                        </el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </div>
                    </template>
                    <template v-else-if="StepsRomeData.active==2">
                        <el-card v-loading="loading" shadow="never" style="width:1360px;height: 710px;">
                            <el-tabs tab-position='left' @tab-click="handleClick" >
                                <el-tab-pane
                                    v-for="item in TestSetRomeData.newTableData"
                                    :disabled="item.state==false"
                                    :key="item.id"
                                    :label="item.stepsName"
                                    :name="item.collectionData">
                                </el-tab-pane>
                                <div v-if="EditCaseRomeData.disPlay">
                                    <div>
                                        <el-row>
                                            <el-col :span="19">
                                                <div style="float:left">
                                                    <el-input placeholder="请输入接口地址" style="width:800px" v-model="EditCaseRomeData.requestUrl">
                                                        <el-select v-model="EditCaseRomeData.requestType" slot="prepend" style="width:97px">
                                                            <el-option
                                                                v-for="item in EditCaseRomeData.requestTypeOption"
                                                                :key="item.value"
                                                                :label="item.label"
                                                                :value="item.value">
                                                            </el-option>
                                                        </el-select>
                                                    </el-input>
                                                </div>
                                            </el-col>
                                            <el-col :span="5">
                                                <div>
                                                    <el-button-group>
                                                        <el-button type="primary" @click="SendRequest()">调试接口</el-button>
                                                        <el-button type="warning" @click="ReferenceOriginalSet()" >引用原设</el-button>
                                                        <el-button icon="el-icon-question" circle plain @click="helpMsg()"></el-button>
                                                    </el-button-group>
                                                </div>
                                            </el-col>
                                        </el-row>
                                    </div>
                                    <div>
                                        <el-tabs v-model="EditCaseRomeData.activeName" @tab-click="handleClickTabs">  
                                            <el-tab-pane :label="EditCaseRomeData.headersName" name="Headers">
                                                <div v-if="EditCaseRomeData.headersRomeData.editModel=='From'">
                                                    <el-table
                                                        :data="EditCaseRomeData.headersRomeData.tableData"
                                                        border
                                                        height="570">
                                                        <el-table-column
                                                            label="启用"
                                                            width="70px"
                                                            align= "center">
                                                            <template slot-scope="scope">
                                                                <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                                            </template>
                                                        </el-table-column>
                                                        <el-table-column
                                                            label="参数名"
                                                            align= "center">
                                                            <template slot-scope="scope">
                                                                <el-input v-model="scope.row.key" placeholder="参数名"></el-input>
                                                            </template>
                                                        </el-table-column>
                                                        <el-table-column
                                                            label="参数值"
                                                            align= "center">
                                                            <template slot-scope="scope">
                                                                <el-input v-model="scope.row.value" placeholder="参数值"></el-input>
                                                            </template>
                                                        </el-table-column>
                                                        <el-table-column
                                                            label="备注"
                                                            align= "center">
                                                            <template slot-scope="scope">
                                                                <el-input v-model="scope.row.remarks" placeholder="备注"></el-input>
                                                            </template>
                                                        </el-table-column>
                                                        <el-table-column
                                                            align="center"
                                                            width="120px">
                                                        <template slot="header">
                                                            <el-button-group>
                                                                <el-button type="success" size="mini" icon="el-icon-circle-plus-outline" @click="CreateNewHeadersData()"></el-button>
                                                                <el-button type="warning" size="mini" @click="changesHeadersEditModel()">Bulk</el-button>
                                                            </el-button-group>
                                                        </template>
                                                        <template slot-scope="scope" style="width:100px">
                                                            <el-button
                                                                size="mini"
                                                                icon="el-icon-delete"
                                                                type="danger"
                                                                @click="handleHeadersDelete(scope.$index, scope.row)"></el-button>
                                                        </template>
                                                        </el-table-column>
                                                    </el-table>
                                                </div>
                                                <div v-else>
                                                    <el-card>
                                                        <div slot="header" style="height:20px">
                                                            <el-row style="margin-top:-8px">
                                                                <el-col :span="12">
                                                                    <div style="float:left;margin-top:3px">
                                                                        <span style="font-size:15px">格式:启用状态,参数名,参数值,备注</span>
                                                                    </div>
                                                                    </el-col>
                                                                <el-col :span="12">
                                                                    <div style="float:right">
                                                                        <el-button type="primary" size="mini" @click="changesHeadersEditModel()">确定</el-button>
                                                                        <el-button size="mini" @click="cancelHeadersBulkEdit()">取消</el-button>
                                                                    </div>
                                                                </el-col>
                                                            </el-row>
                                                        </div>
                                                        <div>
                                                            <el-input
                                                                type="textarea"
                                                                :autosize="{ minRows: 24, maxRows: 24}"
                                                                v-model="EditCaseRomeData.headersRomeData.bulkEdit">
                                                            </el-input>
                                                        </div>
                                                    </el-card>
                                                </div>
                                            </el-tab-pane>
                                            <el-tab-pane :label="EditCaseRomeData.paramsName" name="Params">
                                                <div v-if="EditCaseRomeData.paramsRomeData.editModel=='From'">
                                                    <el-table
                                                        :data="EditCaseRomeData.paramsRomeData.tableData"
                                                        border
                                                        height="610">
                                                        <el-table-column
                                                            label="启用"
                                                            width="70px"
                                                            align= "center">
                                                            <template slot-scope="scope">
                                                                <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                                            </template>
                                                        </el-table-column>
                                                        <el-table-column
                                                            label="参数名"
                                                            align= "center">
                                                            <template slot-scope="scope">
                                                                <el-input v-model="scope.row.key" placeholder="参数名"></el-input>
                                                            </template>
                                                        </el-table-column>
                                                        <el-table-column
                                                            label="参数值"
                                                            align= "center">
                                                            <template slot-scope="scope">
                                                                <el-input v-model="scope.row.value" placeholder="参数值"></el-input>
                                                            </template>
                                                        </el-table-column>
                                                        <el-table-column
                                                            label="备注"
                                                            align= "center">
                                                            <template slot-scope="scope">
                                                                <el-input v-model="scope.row.remarks" placeholder="备注"></el-input>
                                                            </template>
                                                        </el-table-column>
                                                        <el-table-column
                                                            align="center"
                                                            width="120px">
                                                        <template slot="header">
                                                            <el-button-group>
                                                                <el-button type="success" size="mini" icon="el-icon-circle-plus-outline" @click="CreateNewParamsData()"></el-button>
                                                                <el-button type="warning" size="mini" @click="changesParamsEditModel()">Bulk</el-button>
                                                            </el-button-group>
                                                        </template>
                                                        <template slot-scope="scope" style="width:100px">
                                                            <el-button
                                                                size="mini"
                                                                icon="el-icon-delete"
                                                                type="danger"
                                                                @click="handleParamsDelete(scope.$index, scope.row)"></el-button>
                                                        </template>
                                                        </el-table-column>
                                                    </el-table>
                                                </div>
                                                <div v-else>
                                                    <el-card>
                                                        <div slot="header" style="height:20px">
                                                            <el-row style="margin-top:-8px">
                                                                <el-col :span="12">
                                                                    <div style="float:left;margin-top:3px">
                                                                        <span style="font-size:15px">格式:启用状态,参数名,参数值,备注</span>
                                                                    </div>
                                                                    </el-col>
                                                                <el-col :span="12">
                                                                    <div style="float:right">
                                                                        <el-button type="primary" size="mini" @click="changesParamsEditModel()">确定</el-button>
                                                                        <el-button size="mini" @click="cancelParamsBulkEdit()">取消</el-button>
                                                                    </div>
                                                                </el-col>
                                                            </el-row>
                                                        
                                                        </div>
                                                        <div>
                                                            <el-input
                                                                type="textarea"
                                                                :autosize="{ minRows: 24, maxRows: 24}"
                                                                v-model="EditCaseRomeData.paramsRomeData.bulkEdit">
                                                            </el-input>
                                                        </div>
                                                    </el-card>
                                                </div>
                                            </el-tab-pane>
                                            <el-tab-pane :label="EditCaseRomeData.bodyName" name="Body">
                                                <div>
                                                    <el-radio-group v-model="EditCaseRomeData.bodyRomeData.requestSaveType" @change="changeBodyRequestType">
                                                        <el-radio label="none">none</el-radio>
                                                        <el-radio label='form-data'>form-data</el-radio>
                                                        <el-radio label="raw">raw</el-radio>
                                                        <el-radio label="file">file</el-radio>
                                                    </el-radio-group>
                                                </div>
                                                <div v-if="EditCaseRomeData.bodyRomeData.requestSaveType=='none'">
                                                    <el-card shadow="never" class="bodyRome" style="height:580px;">
                                                        <div>该请求没有主体</div>
                                                    </el-card>
                                                </div>
                                                <div v-else-if="EditCaseRomeData.bodyRomeData.requestSaveType=='form-data'">
                                                    <div v-if="EditCaseRomeData.bodyRomeData.editModel=='From'">
                                                        <el-table
                                                            class="bodyRome"
                                                            :data="EditCaseRomeData.bodyRomeData.tableData"
                                                            border
                                                            height="582">
                                                            <el-table-column
                                                                label="启用"
                                                                width="70px"
                                                                align= "center">
                                                                <template slot-scope="scope">
                                                                    <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                                                </template>
                                                            </el-table-column>
                                                            <el-table-column
                                                                label="参数名"
                                                                align= "center">
                                                                <template slot-scope="scope">
                                                                    <el-input v-model="scope.row.key" placeholder="参数名"></el-input>
                                                                </template>
                                                            </el-table-column>
                                                            <el-table-column
                                                                label="参数值"
                                                                align= "center">
                                                                <template slot-scope="scope">
                                                                    <el-input v-model="scope.row.value" placeholder="参数值"></el-input>
                                                                </template>
                                                            </el-table-column>
                                                            <el-table-column
                                                                label="备注"
                                                                align= "center">
                                                                <template slot-scope="scope">
                                                                    <el-input v-model="scope.row.remarks" placeholder="备注"></el-input>
                                                                </template>
                                                            </el-table-column>
                                                            <el-table-column
                                                                align="center"
                                                                width="120px">
                                                            <template slot="header">
                                                                <el-button-group>
                                                                    <el-button type="success" size="mini" icon="el-icon-circle-plus-outline" @click="CreateNewBodyData()"></el-button>
                                                                    <el-button type="warning" size="mini" @click="changesBodyEditModel()">Bulk</el-button>
                                                                </el-button-group>
                                                            </template>
                                                            <template slot-scope="scope" style="width:100px">
                                                                <el-button
                                                                    size="mini"
                                                                    icon="el-icon-delete"
                                                                    type="danger"
                                                                    @click="handleBodyDelete(scope.$index, scope.row)"></el-button>
                                                            </template>
                                                            </el-table-column>
                                                        </el-table>
                                                    </div>
                                                    <div v-else>
                                                        <el-card style="margin-top:5px">
                                                            <div slot="header" style="height:20px;">
                                                                <el-row style="margin-top:-8px">
                                                                    <el-col :span="12">
                                                                        <div style="float:left;margin-top:3px">
                                                                            <span style="font-size:15px">格式:启用状态,参数名,参数值,备注</span>
                                                                        </div>
                                                                        </el-col>
                                                                    <el-col :span="12">
                                                                        <div style="float:right">
                                                                            <el-button type="primary" size="mini" @click="changesBodyEditModel()">确定</el-button>
                                                                            <el-button size="mini" @click="cancelBodyBulkEdit()">取消</el-button>
                                                                        </div>
                                                                    </el-col>
                                                                </el-row>
                                                            </div>
                                                            <div>
                                                                <el-input
                                                                    type="textarea"
                                                                    :autosize="{ minRows: 23, maxRows: 23}"
                                                                    v-model="EditCaseRomeData.bodyRomeData.bulkEdit">
                                                                </el-input>
                                                            </div>
                                                        </el-card>
                                                    </div>
                                                </div>
                                                <div v-else-if="EditCaseRomeData.bodyRomeData.requestSaveType=='raw'">
                                                    <el-input
                                                        class="bodyRome"
                                                        type="textarea"
                                                        :autosize="{ minRows: 27, maxRows: 27}"
                                                        v-model="EditCaseRomeData.bodyRomeData.rawValue">
                                                    </el-input>
                                                </div>
                                                <div v-else>
                                                    <el-card shadow="never" class="bodyRome" style="height:580px;">
                                                        <div>这里是上传文件地址</div>
                                                    </el-card>
                                                </div>
                                            </el-tab-pane>
                                            <el-tab-pane :label="EditCaseRomeData.extractName" name="Extract">
                                                <el-table
                                                    :data="EditCaseRomeData.extractRomeData.tableData"
                                                    border
                                                    height="610">
                                                    <el-table-column
                                                        label="启用"
                                                        width="70px"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="变量名称"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-input v-model="scope.row.key" placeholder="变量名称"></el-input>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="提取表达式"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-input v-model="scope.row.value" placeholder="例:$.statuscode,$.key[0],$.table[0].name"></el-input>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="备注"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-input v-model="scope.row.remarks" placeholder="备注"></el-input>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        align="center"
                                                        width="120px">
                                                    <template slot="header">
                                                        <el-button type="success" size="mini" icon="el-icon-circle-plus-outline" @click="CreateNewExtractData()"></el-button>
                                                    </template>
                                                    <template slot-scope="scope" style="width:100px">
                                                        <el-button
                                                            size="mini"
                                                            icon="el-icon-delete"
                                                            type="danger"
                                                            @click="handleExtractDelete(scope.$index, scope.row)"></el-button>
                                                    </template>
                                                    </el-table-column>
                                                </el-table>
                                            </el-tab-pane>
                                            <el-tab-pane :label="EditCaseRomeData.validateName" name="Validate">
                                                <el-table
                                                    :data="EditCaseRomeData.validateRomeData.tableData"
                                                    border
                                                    height="610">
                                                    <el-table-column
                                                        label="启用"
                                                        width="70px"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="提取变量名称"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-autocomplete
                                                                v-model="scope.row.checkName"
                                                                :fetch-suggestions="fetchSuggestionsValidate"
                                                                placeholder="请输入提取变量名称">
                                                            </el-autocomplete>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="断言类型"
                                                        width="170px"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-select  v-model="scope.row.validateType" placeholder="请选择">
                                                                <el-option
                                                                    v-for="item in EditCaseRomeData.validateRomeData.validateTypeOption"
                                                                    :key="item.value"
                                                                    :label="item.label"
                                                                    :value="item.value">
                                                                </el-option>
                                                            </el-select>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="断言值类型"
                                                        width="120px"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-select v-model="scope.row.valueType"  placeholder="请选择">
                                                                    <el-option
                                                                        v-for="item in EditCaseRomeData.validateRomeData.valueTypeOption"
                                                                        :key="item.value"
                                                                        :label="item.label"
                                                                        :value="item.value">
                                                                    </el-option>
                                                                </el-select>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="预期结果"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-input v-model="scope.row.expectedResults" placeholder="预期结果"></el-input>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="备注"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-input v-model="scope.row.remarks" placeholder="备注"></el-input>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        align="center"
                                                        width="65px">
                                                    <template slot="header">
                                                        <el-button type="success" size="mini" icon="el-icon-circle-plus-outline" @click="CreateNewValidateData()"></el-button>
                                                    </template>
                                                    <template slot-scope="scope" style="width:100px">
                                                    <el-button
                                                        size="mini"
                                                        icon="el-icon-delete"
                                                        type="danger"
                                                        @click="handleValidateDelete(scope.$index, scope.row)"></el-button>
                                                    </template>
                                                    </el-table-column>
                                                </el-table>
                                            </el-tab-pane>
                                            <el-tab-pane :label="EditCaseRomeData.preOperationName" name="PreOperation">
                                                <el-table
                                                    id="PreOperationSort"
                                                    row-key="id"
                                                    :data="EditCaseRomeData.preOperationRomeData.tableData"
                                                    border
                                                    height="610">
                                                    <el-table-column
                                                        label="启用"
                                                        width="70px"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="操作类型"
                                                        width="150px"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-tag type="info">{{scope.row.operationType}}</el-tag>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="操作数据"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <div v-if="scope.row.operationType=='Methods'">
                                                                <el-input v-model.trim="scope.row.methodsName" placeholder="输入DebugTalk文件中需要调用的方法"></el-input>
                                                            </div>
                                                            <div v-else-if="scope.row.operationType=='DataBase'">
                                                                <el-form ref="preOperationRomeData" :model="EditCaseRomeData.preOperationRomeData" label-width="80px">
                                                                    <el-form-item label="数据库:">
                                                                        <el-select v-model="scope.row.dataBase" placeholder="请选择连接的数据库" style="float:left;width:437px">
                                                                            <el-option
                                                                                v-for="item in EditCaseRomeData.preOperationRomeData.dataBaseOptions"
                                                                                :key="item.value"
                                                                                :label="item.label"
                                                                                :value="item.value">
                                                                            </el-option>
                                                                        </el-select>
                                                                    </el-form-item>
                                                                    <el-form-item label="SQL:">
                                                                        <el-input
                                                                            type="textarea"
                                                                            :autosize="{ minRows: 3, maxRows: 3}"
                                                                            v-model="scope.row.sql"
                                                                            placeholder="SQL">
                                                                        </el-input>
                                                                    </el-form-item>
                                                                </el-form>
                                                            </div>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="备注"
                                                        width="300px"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-input v-model="scope.row.remarks" placeholder="备注"></el-input>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        align="center"
                                                        width="100px">
                                                    <template slot="header">
                                                        <el-dropdown @command="handlePreOperationCommand">
                                                            <el-button type="warning" size="mini" icon="el-icon-circle-plus-outline">
                                                                <i class="el-icon-arrow-down el-icon--right"></i>
                                                            </el-button>
                                                            <el-dropdown-menu slot="dropdown">
                                                                <el-dropdown-item command="Methods">方法函数</el-dropdown-item>
                                                                <el-dropdown-item command="DataBase">数据库操作</el-dropdown-item>
                                                            </el-dropdown-menu>
                                                        </el-dropdown>
                                                    </template>
                                                    <template slot-scope="scope" style="width:100px">
                                                        <el-button
                                                            size="mini"
                                                            icon="el-icon-delete"
                                                            type="danger"
                                                            @click="handlePreOperationDelete(scope.$index, scope.row)"></el-button>
                                                    </template>
                                                    </el-table-column>
                                                </el-table>
                                            </el-tab-pane>
                                            <el-tab-pane :label="EditCaseRomeData.rearOperationName" name="RearOperation">
                                                <el-table
                                                    id="RearOperationSort"
                                                    row-key="id"
                                                    :data="EditCaseRomeData.rearOperationRomeData.tableData"
                                                    border
                                                    height="610">
                                                    <el-table-column
                                                        label="启用"
                                                        width="70px"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-switch v-model="scope.row.state" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="操作类型"
                                                        width="150px"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-tag type="info">{{scope.row.operationType}}</el-tag>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="操作数据"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <div v-if="scope.row.operationType=='Methods'">
                                                                <el-input v-model.trim="scope.row.methodsName" placeholder="输入DebugTalk文件中需要调用的方法"></el-input>
                                                            </div>
                                                            <div v-else-if="scope.row.operationType=='DataBase'">
                                                                <el-form ref="rearOperationRomeData" :model="EditCaseRomeData.rearOperationRomeData" label-width="80px">
                                                                    <el-form-item label="数据库:">
                                                                        <el-select v-model="scope.row.dataBase" placeholder="请选择连接的数据库" style="float:left;width:437px">
                                                                            <el-option
                                                                                v-for="item in EditCaseRomeData.rearOperationRomeData.dataBaseOptions"
                                                                                :key="item.value"
                                                                                :label="item.label"
                                                                                :value="item.value">
                                                                            </el-option>
                                                                        </el-select>
                                                                    </el-form-item>
                                                                    <el-form-item label="SQL:">
                                                                        <el-input
                                                                            type="textarea"
                                                                            :autosize="{ minRows: 3, maxRows: 3}"
                                                                            v-model="scope.row.sql"
                                                                            placeholder="SQL">
                                                                        </el-input>
                                                                    </el-form-item>
                                                                </el-form>
                                                            </div>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        label="备注"
                                                        width="300px"
                                                        align= "center">
                                                        <template slot-scope="scope">
                                                            <el-input v-model="scope.row.remarks" placeholder="备注"></el-input>
                                                        </template>
                                                    </el-table-column>
                                                    <el-table-column
                                                        align="center"
                                                        width="100px">
                                                    <template slot="header">
                                                        <el-dropdown @command="handleRearOperationCommand">
                                                            <el-button type="warning" size="mini" icon="el-icon-circle-plus-outline">
                                                                <i class="el-icon-arrow-down el-icon--right"></i>
                                                            </el-button>
                                                            <el-dropdown-menu slot="dropdown">
                                                                <el-dropdown-item command="Methods">方法函数</el-dropdown-item>
                                                                <el-dropdown-item command="DataBase">数据库操作</el-dropdown-item>
                                                            </el-dropdown-menu>
                                                        </el-dropdown>
                                                    </template>
                                                    <template slot-scope="scope" style="width:100px">
                                                        <el-button
                                                            size="mini"
                                                            icon="el-icon-delete"
                                                            type="danger"
                                                            @click="handleRearOperationDelete(scope.$index, scope.row)"></el-button>
                                                    </template>
                                                    </el-table-column>
                                                </el-table>
                                            </el-tab-pane>
                                        </el-tabs>
                                    </div>
                                </div>
                            </el-tabs>
                          </el-card>
                    </template>
                    <template v-else>
         
                    </template>
                </el-card>
                <el-button style="margin-top: 12px;" icon="el-icon-arrow-left" type="primary" v-if="StepsRomeData.disPlay_Previous" @click="previous">上一步</el-button>
                <el-button style="margin-top: 12px;" type="primary" v-if="StepsRomeData.disPlay_Next" @click="next">下一步<i class="el-icon-arrow-right el-icon--right"></i></el-button>
                <el-button style="margin-top: 12px;" type="success" v-if="StepsRomeData.disPlay_Save" @click="DataSave()">保存</el-button>
            </el-drawer>
        </template>
        <template>
            <dialog-api-main
                @closeDialog="closeApiMainDialog" 
                :isVisible="dialog.apiMain.dialogVisible" 
                :dialogPara="dialog.apiMain.dialogPara"
                @getData="AddToTestSetTable($event)">
            </dialog-api-main>
        </template>
    </div>
</template>

<script>
import Qs from 'qs';
import Sortable from 'sortablejs';
import {PrintConsole} from "../../../../../../js/Logger.js";
import {GetPageNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetFunNameItems} from "../../../../../../js/GetSelectTable.js";
import {GetPageEnvironmentNameItems} from "../../../../../../js/GetSelectTable.js";

import DialogApiMain from "./ApiMain.vue";


export default {
    components: {
        DialogApiMain
    },
    data() {
        return {
            dialogTitle:"",
            dialogVisible:false,
            isAddNew:true,//是否是新增窗口
            loading:false,
            StepsRomeData:{
                active:0,
                stepLength:3,//步长，整个窗口可以执行的步骤数
                processStatus:'process',
                disPlay_Save:false,
                disPlay_Next:true,
                disPlay_Previous:false,
            },
            BasicRomeData:{
                pageId:'',
                pageNameOption:[],
                funId:'',
                funNameOption:[],
                labelId:'',
                labelNameOption:[
                    {'label':'普通用例','value':'CommonCase'},
                    {'label':'回归用例','value':'ReturnCase'},
                ],
                testType:'',
                testTypeOption:[
                    {'label':'单元测试','value':'UnitTest'},
                    {'label':'混合测试','value':'HybridTest'},
                ],
                caseState:'',
                caseStateOption:[
                    {'label':'研发中','value':'InDev'},
                    {'label':'已完成','value':'Completed'},
                    {'label':'弃用','value':'Discard'},
                ],
                environmentId:'',
                environmentNameOption:[],
                caseName:'',
                priorityId:'',//优先级
                priorityNameOption:[
                    {'label':'P0','value':'P0','details':'最高'},
                    {'label':'P1','value':'P1','details':'高'},
                    {'label':'P2','value':'P2','details':'中'},
                    {'label':'P3','value':'P3','details':'低'},
                ],
                rules:{
                    pageId:[{ required: true, message: '请选择所属页面', trigger: 'change' }],
                    funId:[{ required: true, message: '请选择所属功能', trigger: 'change' }],
                    environmentId:[{ required: true, message: '请选择页面环境', trigger: 'change' }],
                    testType:[{ required: true, message: '请选择测试类型', trigger: 'change' }],
                    labelId:[{ required: true, message: '请选择用例标签', trigger: 'change' }],
                    priorityId:[{ required: true, message: '请选择优先级', trigger: 'change' }],
                    caseName:[
                        { required: true, message: '请输入用例名称', trigger: 'blur' },
                        { min: 1, max: 15, message: '长度在 1 到 15 个字符', trigger: 'blur' }
                    ],
                    caseState:[{ required: true, message: '请选择用例状态', trigger: 'change' }],
                },
            },
            TestSetRomeData:{
                tableData:[],//测试集数据
                newTableData:[]//重新组合测试集数据
            },
            EditCaseRomeData:{
                disPlay:false,
                tableData:[],//最终数据保存在这里
                apiId:'',//
                requestUrl:'',
                requestType:'GET',
                requestTypeOption:[
                    {'label':'GET','value':'GET'},
                    {'label':'POST','value':'POST'},
                ],
                activeName:'Headers',

                headersName:'Headers',
                headersRomeData:{
                    index:0,
                    tableData:[],
                    editModel:'From',
                    bulkEdit:'',//显示给屏幕上看的数据
                },

                paramsName:'Params',
                paramsRomeData:{
                    index:0,
                    tableData:[],
                    editModel:'From',
                    bulkEdit:'',//显示给屏幕上看的数据
                },

                bodyName:'Body',
                bodyRomeData:{
                    index:0,
                    tableData:[],
                    editModel:'From',
                    bulkEdit:'',
                    requestSaveType:'form-data',//请求保存类型，none,form-data,json,raw
                    rawValue:'',
                },

                extractName:'Extract/提取',
                extractRomeData:{
                    index:0,
                    tableData:[],
                },

                validateName:'Validate/断言',
                validateRomeData:{
                    index:0,
                    tableData:[],
                    validateTypeOption:[//断言类型
                        {label: 'equals(==)', value: 'equals'},
                        {label: 'contains(In)',value: 'contains'},
                        {label: 'not_equals(!=)', value: 'not_equals'},
                    ],
                    valueTypeOption:[//对比值类型
                        {label: 'String',value: 'str'},
                        {label: 'Int',value: 'int'},
                        {label: 'Float',value: 'float'},
                        {label: 'Bool',value: 'bool'},
                        {label: 'List',value: 'list'}
                    ],
                },

                preOperationName:'前置操作',
                preOperationRomeData:{
                    index:0,
                    tableData:[],
                    dataBaseOptions:[],
                },

                rearOperationName:'后置操作',
                rearOperationRomeData:{
                    index:0,
                    tableData:[],
                    dataBaseOptions:[],
                }


            },
            dialog:{
                apiMain:{
                    dialogVisible:false,
                    dialogPara:{
                        dialogTitle:"",//初始化标题
                        isAddNew:true,//初始化是否新增\修改
                    },
                },
            }

        };
    },
    mounted(){

    },
    computed:{//计算属性

    },
    props:[//main页面在引用editor时 必须声明所需要调用的属性
        'isVisible','dialogPara'
    ],
    watch:{//当我们输入值后，wacth监听每次修改变化的新值，然后计算输出值
        isVisible:{//用于监听父页面的isVisible，true时就弹出窗口
            handler(newval,oldval)
            {
                this.dialogVisible=newval;  
            }
        },
        dialogPara:{
            handler(newval,oldval)
            {
                PrintConsole(newval);
                this.ClearStepsRomeData();
                this.ClearBasicRomeData();
                this.ClearTestSetRomeData();
                this.ClearEditRomeData();
                this.EditCaseRomeData.apiId='';
                this.EditCaseRomeData.tableData =[];
                
                this.dialogTitle = newval.dialogTitle;
                this.isAddNew = newval.isAddNew;

                if(newval.isAddNew==false){//进入编辑状态
                
                  
                }
            }
        },
        'StepsRomeData.active': function (newVal,oldVal) {//监听所属项目有变化
            // console.log('newVal:'+newVal)
            let self = this;
            if(newVal==0){
                self.StepsRomeData.disPlay_Save = false;
                self.StepsRomeData.disPlay_Next = true;
                self.StepsRomeData.disPlay_Previous = false;
                self.EditCaseRomeData.disPlay=false;
               
            }else if(newVal==1 || newVal==2){
                self.StepsRomeData.disPlay_Save = false;
                self.StepsRomeData.disPlay_Previous = true;
                self.StepsRomeData.disPlay_Next = true;
                self.EditCaseRomeData.disPlay=false;
            }else{
                self.StepsRomeData.disPlay_Save = true;
                self.StepsRomeData.disPlay_Next = false;
                self.StepsRomeData.disPlay_Previous = true;
                self.EditCaseRomeData.disPlay=false;
                
            }
            PrintConsole('步骤',this.StepsRomeData.active)
        },
        'BasicRomeData.pageId': function (newVal,oldVal) {//监听所属项目有变化的话就清空所属模块
            let self = this;
            if(newVal!=oldVal){
                self.BasicRomeData.funId='';
                self.BasicRomeData.funNameOption=[];
            }
        },
        'EditCaseRomeData.headersRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.EditCaseRomeData.headersRomeData.tableData.length;
                if(dataLength==0){
                    self.EditCaseRomeData.headersName='Headers';
                }else{
                    self.EditCaseRomeData.headersName='Headers('+dataLength+')';
                }  
            }
        },
        'EditCaseRomeData.paramsRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.EditCaseRomeData.paramsRomeData.tableData.length;
                if(dataLength==0){
                    self.EditCaseRomeData.paramsName='Params';
                }else{
                    self.EditCaseRomeData.paramsName='Params('+dataLength+')';
                }
                
            }
        },
        'EditCaseRomeData.bodyRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.EditCaseRomeData.bodyRomeData.tableData.length;
                if(dataLength==0){
                    self.EditCaseRomeData.bodyName='Body';
                }else{
                    self.EditCaseRomeData.bodyName='Body('+dataLength+')';
                }
                
            }
        },
        'EditCaseRomeData.extractRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.EditCaseRomeData.extractRomeData.tableData.length;
                if(dataLength==0){
                    self.EditCaseRomeData.extractName='Extract/提取';
                }else{
                    self.EditCaseRomeData.extractName='Extract/提取('+dataLength+')';
                }
                
            }
        },
        'EditCaseRomeData.validateRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.EditCaseRomeData.validateRomeData.tableData.length;
                if(dataLength==0){
                    self.EditCaseRomeData.validateName='Validate/断言';
                }else{
                    self.EditCaseRomeData.validateName='Validate/断言('+dataLength+')';
                }
                
            }
        },
        'EditCaseRomeData.preOperationRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.EditCaseRomeData.preOperationRomeData.tableData.length;
                if(dataLength==0){
                    self.EditCaseRomeData.preOperationName='前置操作';
                }else{
                    self.EditCaseRomeData.preOperationName='前置操作('+dataLength+')';
                }
                
            }
        },
        'EditCaseRomeData.rearOperationRomeData.index': function (newVal,oldVal) {//实时更新当前有多少个数据到标题上
            let self = this;
            if(newVal!=oldVal){
                let dataLength = self.EditCaseRomeData.rearOperationRomeData.tableData.length;
                if(dataLength==0){
                    self.EditCaseRomeData.rearOperationName='后置操作';
                }else{
                    self.EditCaseRomeData.rearOperationName='后置操作('+dataLength+')';
                }
                
            }
        },
    },
    methods: {
        dialogClose(done){//用于调用父页面方法
            this.$emit('closeDialog');
        },
        //导航条事件
        next() {//下一步
            let self = this;
            if(self.StepsRomeData.active==0){//基本用例数据
                self.StepsRomeData.active++;
                // this.$refs['BasicCase'].validate((valid) => {
                //     if (valid) {//通过
                //         self.StepsRomeData.active++;
                //         self.$nextTick(function () {//当DOM加载完成后才会执行这个!
                //             self.rowDrop();
                //         })
                //     } 
                // });
            }else if(self.StepsRomeData.active==1){
                if(self.TestSetRomeData.tableData.length<1){
                    self.$message.warning('当前至少新增1条接口数据!');
                }else{
                    self.StepsRomeData.active++;
                    self.againCombinationTestSet();//重新组合测试集
                    PrintConsole(self.TestSetRomeData.tableData);
                }
            }else{
                if(self.EditCaseRomeData.requestUrl){//因为在下一步的时候会清空数据,所以这里用来卡住多次重复上下一步保存的问题
                    self.SaveCurrentRomeData();
                }
                self.UpdateTestNameToTable();
                self.ClearEditRomeData();
                PrintConsole('最终列表数据',self.EditCaseRomeData.tableData);
                self.StepsRomeData.active++;
            }
            // PrintConsole('步骤',this.StepsRomeData.active)
        },
        previous(){//上一步
            let self = this;
            self.StepsRomeData.processStatus='process';
            self.StepsRomeData.active--;
            if(self.StepsRomeData.active==3){
                self.StepsRomeData.active--;
            }else if(self.StepsRomeData.active==1){
                // self.$nextTick(function () {//当DOM加载完成后才会执行这个!
                //     self.rowDrop();
                // })
            }
            // PrintConsole('步骤',self.StepsRomeData.active)
        },
        ClearStepsRomeData(){
            let self = this;
            // self.resetForm('RomeData');
            self.StepsRomeData.active= 0;
            self.StepsRomeData.disPlay_Save = false;
            self.StepsRomeData.disPlay_Next = true;
            self.StepsRomeData.processStatus ='process';
           
        },
        returnToMain(){
            let self = this;
            self.dialogVisible = false;//关闭新增弹窗
            self.$emit('closeDialog');
            self.$emit('Succeed');//回调查询   
        },

        //基础信息
        ClearBasicRomeData(){
            let self = this;
            self.resetForm('BasicRomeData');
            self.BasicRomeData.pageId='';
            self.BasicRomeData.funId='';
            self.BasicRomeData.environmentId='';
            self.BasicRomeData.testType='';
            self.BasicRomeData.labelId='';
            self.BasicRomeData.priorityId='';
            self.BasicRomeData.caseName='';
            self.BasicRomeData.caseState='';
        },
        GetPageNameOption(){
            GetPageNameItems(this.$cookies.get('proId')).then(d=>{
                this.BasicRomeData.pageNameOption = d;
            });
        },
        GetFunNameOption(){
            this.BasicRomeData.funNameOption = [];
            if(this.BasicRomeData.pageId){
                GetFunNameItems(this.$cookies.get('proId'),this.BasicRomeData.pageId).then(d=>{
                    this.BasicRomeData.funNameOption = d;
                });
            }else{
                this.$message.warning('请先选择所属页面!');
            }
        },
        GetPageEnvironmentNameOption(){
            GetPageEnvironmentNameItems(this.$cookies.get('proId')).then(d=>{
                this.BasicRomeData.environmentNameOption = d;
            });
        },
        resetForm(formName) {//清除正则验证
            if (this.$refs[formName] !== undefined) {
                console.log('清除正则验证')
                this.$refs[formName].resetFields();
            }
        },

        //组合测试集
        ClearTestSetRomeData(){
            let self = this;
            self.TestSetRomeData.tableData=[];
            self.TestSetRomeData.newTableData=[];
        },
        closeApiMainDialog(){
            this.dialog.apiMain.dialogVisible = false;
        },
        OpenApiMainDialog(){
            let self = this;
            self.dialog.apiMain.dialogPara={
                dialogTitle:"导入接口",//初始化标题
                pageId:self.BasicRomeData.pageId,
                funId:self.BasicRomeData.funId,
            }
            self.dialog.apiMain.dialogVisible=true;
        },
        AddToTestSetTable(data){
            let self = this;
            PrintConsole('回调数据:',data);
            //将重复的id给用 id-次数来处理
            let findCount = 0;
            data.forEach(item=>{
                let apiId = null;
                self.TestSetRomeData.tableData.forEach((d,i)=>{
                    if(d.id == item.id || d.id == item.id+'-'+findCount){
                        findCount++;
                    }
                });
                if(findCount!=0){
                    apiId=item.id+'-'+findCount;
                }else{
                    apiId=item.id;
                }
                let obj = {};
                obj.id=String(apiId);
                obj.state=true;
                obj.apiName=item.apiName;
                obj.apiState = item.apiState;
                obj.testName='';
                obj.is_synchronous=false;
                self.TestSetRomeData.tableData.push(obj);
            });
            self.rowDrop();
            PrintConsole('AddToTestSetTable:',self.TestSetRomeData.tableData);
        },
        handleDelete(index,row){//删除独条的步骤
            let self = this;
            let tableData = [];
            self.TestSetRomeData.tableData.splice(index,1);
            self.EditCaseRomeData.tableData.forEach((d,i)=>{
                if(d.apiId==row.id){
                }else{
                    tableData.push(d);
                }
            });
            self.EditCaseRomeData.tableData = tableData;
            self.EditCaseRomeData.apiId="";
            self.ClearEditRomeData();
            PrintConsole('最终数据',self.EditCaseRomeData.tableData);
        },
        rowDrop() {//排序方法
            PrintConsole('加载可拖动效果')
            const tbody = document.querySelector('#TestSet > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(2)');
            let self = this;
            Sortable.create(tbody, {
                onEnd ({ newIndex, oldIndex }) {
                    const currRow = self.TestSetRomeData.tableData.splice(oldIndex, 1)[0];
                    self.TestSetRomeData.tableData.splice(newIndex, 0, currRow);
                    // console.log(self.RomeData.TableData);
                }
            });
        },
        againCombinationTestSet(){//重新组合测试集
            let self = this;
            self.TestSetRomeData.newTableData = [];
            self.TestSetRomeData.tableData.forEach(d=>{
                let obj = {};
                obj.id=d.id;
                obj.state=d.state;
                let stepsName = '';
                if(d.testName){
                    stepsName = d.apiName+'('+d.testName+')';
                }else{
                    stepsName = d.apiName;
                }
                obj.stepsName=stepsName;
                obj.collectionData = 'apiId:'+d.id+','+'testName:'+d.testName+','+'synchronous:'+d.is_synchronous+','+'apiState:'+d.state;
                self.TestSetRomeData.newTableData.push(obj);
            });
        },

        //编写测试用例
        handleClick(tab, event){//点击左侧菜单数据
            PrintConsole(tab);
            let self = this;
            
            self.EditCaseRomeData.disPlay=true;
            let tabData = tab.name.split(',');
            let apiId = tabData[0].split(':')[1];
            let testName = tabData[1].split(':')[1]//测试名称
            let synchronous = tabData[2].split(':')[1]; //是否开启同步
            let apiState = tabData[3].split(':')[1];  //接口是否启用
            let tempCaseTable = null;
           
            
            PrintConsole('apiId',apiId);
            PrintConsole('上次的ApiId',self.EditCaseRomeData.apiId);
            PrintConsole('testName',testName);
            PrintConsole('synchronous',synchronous);
            PrintConsole('apiState',apiState);

            //第一次点击的时候是没有apiId值的,所以直接不处理
            //在点击切换接口的时候 这里会把上一次的数据保存到最终列表中
            if(self.EditCaseRomeData.apiId){
                //点击左侧的接口名称的时候 查询当前的数据有没有保存到列表中
                tempCaseTable = self.EditCaseRomeData.tableData.find(item=>
                    item.apiId == self.EditCaseRomeData.apiId//这个ID在第一次点击的时候是为空的,每一次点击是显示上一次的点击的ID
                );
                if(tempCaseTable){//如果保存到列表中了,就覆盖保存一次
                    self.EditCaseRomeData.tableData.forEach((d,i)=>{
                        if(d.apiId==self.EditCaseRomeData.apiId){
                            self.EditCaseRomeData.tableData[i].requestType =self.EditCaseRomeData.requestType;
                            self.EditCaseRomeData.tableData[i].requestUrl =self.EditCaseRomeData.requestUrl;
                            
                            self.EditCaseRomeData.tableData[i].headers =self.EditCaseRomeData.headersRomeData.tableData;
                            self.EditCaseRomeData.tableData[i].params =self.EditCaseRomeData.paramsRomeData.tableData;

                            self.EditCaseRomeData.tableData[i].body.requestSaveType =self.EditCaseRomeData.bodyRomeData.requestSaveType;
                            self.EditCaseRomeData.tableData[i].body.tableData =self.EditCaseRomeData.bodyRomeData.tableData;
                            self.EditCaseRomeData.tableData[i].body.rawValue =self.EditCaseRomeData.bodyRomeData.rawValue;

                            self.EditCaseRomeData.tableData[i].extract.tableData =self.EditCaseRomeData.extractRomeData.tableData;
                            self.EditCaseRomeData.tableData[i].validate.tableData =self.EditCaseRomeData.validateRomeData.tableData;

                            self.EditCaseRomeData.tableData[i].preOperation.tableData =self.EditCaseRomeData.preOperationRomeData.tableData;
                            self.EditCaseRomeData.tableData[i].rearOperation.tableData =self.EditCaseRomeData.rearOperationRomeData.tableData;
                        }
                    });
                    PrintConsole('覆盖数据id:',self.EditCaseRomeData.apiId);
                }else{//如果没有保存到列表的话就保存进去
                    //新增前先查询下测试集中有没有此数据的ID,如果没有的话就不会新增
                    let tempTestSet= self.TestSetRomeData.tableData.find(item=>
                        item.id == self.EditCaseRomeData.apiId//这个ID在第一次点击的时候是为空的,每一次点击是显示上一次的点击的ID
                    );
                    if(tempTestSet){
                        let obj = {};
                        obj.apiId = self.EditCaseRomeData.apiId;
                        obj.requestType = self.EditCaseRomeData.requestType;
                        obj.requestUrl = self.EditCaseRomeData.requestUrl;
                        obj.headers = self.EditCaseRomeData.headersRomeData.tableData;
                        obj.params = self.EditCaseRomeData.paramsRomeData.tableData;
                        obj.body = {
                            'tableData':self.EditCaseRomeData.bodyRomeData.tableData,
                            'requestSaveType':self.EditCaseRomeData.bodyRomeData.requestSaveType,
                            'rawValue':self.EditCaseRomeData.bodyRomeData.rawValue,
                            }
                        obj.extract = self.EditCaseRomeData.extractRomeData.tableData;
                        obj.validate = self.EditCaseRomeData.validateRomeData.tableData;
                        obj.preOperation = self.EditCaseRomeData.preOperationRomeData.tableData;
                        obj.rearOperation = self.EditCaseRomeData.rearOperationRomeData.tableData;


                        self.EditCaseRomeData.tableData.push(obj);
                        PrintConsole('新增数据id:',self.EditCaseRomeData.apiId);
                        PrintConsole('新增数据:',self.EditCaseRomeData.tableData);
                    }
                }
            }

            

            //查询当前保存的列表中的数据有没有相同的
            tempCaseTable = self.EditCaseRomeData.tableData.find(item=>
                item.apiId == apiId
            );
            if(tempCaseTable){//如果有相同的就赋值到当前页面中
                if(synchronous=='true'){//看当前是不是开了同步,如果开了就把接口的值赋值到页面上
                    self.LoadApiData(apiId);
                    PrintConsole('开始了同步,赋值到页面');
                    self.ClearEditRomeData();
                }else{
                    self.ClearEditRomeData();
                    self.EditCaseRomeData.tableData.forEach((d,i)=>{
                        if(d.apiId==tempCaseTable.apiId){
                            self.EditCaseRomeData.requestType = self.EditCaseRomeData.tableData[i].requestType;
                            self.EditCaseRomeData.requestUrl = self.EditCaseRomeData.tableData[i].requestUrl;

                            self.EditCaseRomeData.headersRomeData.index = self.EditCaseRomeData.tableData[i].headers.length;
                            self.EditCaseRomeData.headersRomeData.tableData = self.EditCaseRomeData.tableData[i].headers;

                            self.EditCaseRomeData.paramsRomeData.index = self.EditCaseRomeData.tableData[i].params.length;
                            self.EditCaseRomeData.paramsRomeData.tableData = self.EditCaseRomeData.tableData[i].params;

                            self.EditCaseRomeData.bodyRomeData.requestSaveType = self.EditCaseRomeData.tableData[i].body.requestSaveType;
                            self.EditCaseRomeData.bodyRomeData.index = self.EditCaseRomeData.tableData[i].body.length;
                            self.EditCaseRomeData.bodyRomeData.tableData= self.EditCaseRomeData.tableData[i].body.tableData;
                            self.EditCaseRomeData.bodyRomeData.rawValue = self.EditCaseRomeData.tableData[i].body.rawValue;

                            self.EditCaseRomeData.extractRomeData.index = self.EditCaseRomeData.tableData[i].extract.length;
                            self.EditCaseRomeData.extractRomeData.tableData = self.EditCaseRomeData.tableData[i].extract.tableData;

                            self.EditCaseRomeData.validateRomeData.index = self.EditCaseRomeData.tableData[i].validate.length;
                            self.EditCaseRomeData.validateRomeData.tableData = self.EditCaseRomeData.tableData[i].validate.tableData;

                            self.EditCaseRomeData.preOperationRomeData.index = self.EditCaseRomeData.tableData[i].preOperation.length;
                            self.EditCaseRomeData.preOperationRomeData.tableData = self.EditCaseRomeData.tableData[i].preOperation.tableData;

                            self.EditCaseRomeData.rearOperationRomeData.index = self.EditCaseRomeData.tableData[i].rearOperation.length;
                            self.EditCaseRomeData.rearOperationRomeData.tableData = self.EditCaseRomeData.tableData[i].rearOperation.tableData;

                            PrintConsole('赋值到页面:',apiId);
                        }
                    });
                }   
            }else{//如果没有相同的就不管
                //第1次进这个页面的时候会到这里
                if(synchronous=='true'){//看当前是不是开了同步,如果开了就把接口的值赋值到页面上
                    //不会同步已存在的数据
                    self.LoadApiData(apiId);
                    PrintConsole('开始了同步,赋值到页面');
                    self.ClearEditRomeData();
                }else{
                    self.ClearEditRomeData();
                }
            }

            PrintConsole('当前列表数据:',self.EditCaseRomeData.tableData);
            self.EditCaseRomeData.apiId = apiId;
        },
        handleClickTabs(tab, event){//点击头部主体等标签
            PrintConsole(tab);
        },
        ClearEditRomeData(){
            PrintConsole('ClearEditRomeData');
            let self = this;
            self.EditCaseRomeData.requestType='GET';
            self.EditCaseRomeData.requestUrl='';
            self.EditCaseRomeData.activeName='Headers';
            self.EditCaseRomeData.headersName='Headers';
            self.EditCaseRomeData.paramsName='Params';
            self.EditCaseRomeData.bodyName='Body';
            self.EditCaseRomeData.extractName='Extract/提取';
            self.EditCaseRomeData.validateName='Validate/断言';
            self.EditCaseRomeData.preOperationName='前置操作';
            self.EditCaseRomeData.rearOperationName='后置操作';

            // //headersRomeData
            // self.EditCaseRomeData.headersRomeData.tableData=[];
            // self.EditCaseRomeData.headersRomeData.index=0;
            // self.EditCaseRomeData.headersRomeData.editModel='From';

            // // //paramsRomeData
            // self.EditCaseRomeData.paramsRomeData.tableData=[];
            // self.EditCaseRomeData.paramsRomeData.index=0;
            // self.EditCaseRomeData.paramsRomeData.editModel='From';

            // //bodyRomeData
            // self.EditCaseRomeData.bodyRomeData.tableData=[];
            // self.EditCaseRomeData.bodyRomeData.index=0;
            // self.EditCaseRomeData.bodyRomeData.editModel='From';
            // self.EditCaseRomeData.bodyRomeData.requestSaveType='form-data';
            // self.EditCaseRomeData.bodyRomeData.rawValue = '';

            // //extractRomeData
            // self.EditCaseRomeData.extractRomeData.tableData=[];
            // self.EditCaseRomeData.extractRomeData.index=0;

            // //validateRomeData
            // self.EditCaseRomeData.validateRomeData.tableData=[];
            // self.EditCaseRomeData.validateRomeData.index=0;

            // //PreOperationRomeData
            // self.EditCaseRomeData.preOperationRomeData.tableData=[];
            // self.EditCaseRomeData.preOperationRomeData.index=0;

            // //rearOperationRomeData
            // self.EditCaseRomeData.rearOperationRomeData.tableData=[];
            // self.EditCaseRomeData.rearOperationRomeData.index=0;
        },
        // ReferenceOriginalSet(){//引用原设
        //     let self = this;
        //     self.$confirm('引用原接口设置,会清空当前您所填写的参数,请确定是否引用?', '提示', {
        //         confirmButtonText: '确定',
        //         cancelButtonText: '取消',
        //         type: 'warning'
        //         }).then(() => {
        //             self.ClearEditRomeData();
        //             self.loading=true;
        //             self.$axios.get('/api/ApiIntMaintenance/LoadData',{
        //                 params:{
        //                     'apiId':self.EditCaseRomeData.apiId
        //                 }
        //             }).then(res => {
        //                 if(res.data.statusCode==2000){
        //                     self.EditCaseRomeData.requestType=res.data.apiInfo.requestType;
        //                     self.EditCaseRomeData.requestUrl=res.data.apiInfo.currentRequestUrl;
                        
        //                     //headers
        //                     res.data.apiInfo.request.headers.forEach(item_headers=>{
        //                         let obj = {};
        //                         obj.index = item_headers.index;
        //                         obj.state =item_headers.state;
        //                         obj.key =item_headers.key;
        //                         obj.value=item_headers.value;
        //                         obj.remarks=item_headers.remarks;

        //                         self.EditCaseRomeData.headersRomeData.tableData.push(obj);
        //                     });
        //                     self.EditCaseRomeData.headersRomeData.index=res.data.apiInfo.request.headers.length+1;

        //                     //params
        //                     res.data.apiInfo.request.params.forEach(item_params=>{
        //                         let obj = {};
        //                         obj.index = item_params.index;
        //                         obj.state =item_params.state;
        //                         obj.key =item_params.key;
        //                         obj.value=item_params.value;
        //                         obj.remarks=item_params.remarks;
        //                         self.EditCaseRomeData.paramsRomeData.tableData.push(obj);
        //                     });
        //                     self.EditCaseRomeData.paramsRomeData.index=res.data.apiInfo.request.params.length+1;

        //                     //body
        //                     self.EditCaseRomeData.bodyRomeData.requestSaveType = res.data.apiInfo.request.body.requestSaveType;
        //                     if(res.data.apiInfo.request.body.requestSaveType=='form-data'){
        //                         res.data.apiInfo.request.body.bodyData.forEach(item_body=>{
        //                             let obj = {};
        //                             obj.index = item_body.index;
        //                             obj.state =item_body.state;
        //                             obj.key =item_body.key;
        //                             obj.value=item_body.value;
        //                             obj.remarks=item_body.remarks;
        //                             self.EditCaseRomeData.bodyRomeData.tableData.push(obj);
        //                         });
        //                         self.EditCaseRomeData.bodyRomeData.index=res.data.apiInfo.request.body.bodyData.length+1;
        //                     }else if(res.data.apiInfo.request.body.requestSaveType=='raw'){
        //                         self.EditCaseRomeData.bodyRomeData.rawValue = res.data.apiInfo.request.body.bodyData;
        //                     }
                    
        //                     //extract
        //                     res.data.apiInfo.request.extract.forEach(item_extract=>{
        //                         let obj = {};
        //                         obj.index = item_extract.index;
        //                         obj.state =item_extract.state;
        //                         obj.key =item_extract.key;
        //                         obj.value=item_extract.value;
        //                         obj.remarks=item_extract.remarks;
        //                         self.EditCaseRomeData.extractRomeData.tableData.push(obj);
        //                     });
        //                     self.EditCaseRomeData.extractRomeData.index=res.data.apiInfo.request.extract.length+1;

        //                     //validate
        //                     res.data.apiInfo.request.validate.forEach(item_validate=>{
        //                         let obj = {};
        //                         obj.index = item_validate.index;
        //                         obj.state =item_validate.state;
        //                         obj.checkName =item_validate.checkName;
        //                         obj.validateType=item_validate.validateType;
        //                         obj.valueType=item_validate.valueType;
        //                         obj.expectedResults=item_validate.expectedResults;
        //                         obj.remarks=item_validate.remarks;
        //                         self.EditCaseRomeData.validateRomeData.tableData.push(obj);
        //                     });
        //                     self.EditCaseRomeData.validateRomeData.index=res.data.apiInfo.request.validate.length+1;

        //                     //preOperation
        //                     res.data.apiInfo.request.preOperation.forEach(item_preOperation=>{
        //                         let obj = {};
        //                         obj.index = item_preOperation.index;
        //                         obj.state =item_preOperation.state;
        //                         obj.operationType =item_preOperation.operationType;
        //                         obj.methodsName=item_preOperation.methodsName;
        //                         obj.dataBase=item_preOperation.dataBase;
        //                         obj.sql=item_preOperation.sql;
        //                         obj.remarks=item_preOperation.remarks;

        //                         self.EditCaseRomeData.preOperationRomeData.tableData.push(obj);
        //                     });
        //                     self.EditCaseRomeData.preOperationRomeData.index=res.data.apiInfo.request.preOperation.length+1;

        //                     //rearOperation
        //                     res.data.apiInfo.request.rearOperation.forEach(item_rearOperation=>{
        //                         let obj = {};
        //                         obj.index = item_rearOperation.index;
        //                         obj.state =item_rearOperation.state;
        //                         obj.operationType =item_rearOperation.operationType;
        //                         obj.methodsName=item_rearOperation.methodsName;
        //                         obj.dataBase=item_rearOperation.dataBase;
        //                         obj.sql=item_rearOperation.sql;
        //                         obj.remarks=item_rearOperation.remarks;

        //                         self.EditCaseRomeData.rearOperationRomeData.tableData.push(obj);
        //                     });
        //                     self.EditCaseRomeData.rearOperationRomeData.index=res.data.apiInfo.request.rearOperation.length+1;
        //                     self.loading=false;
        //                 }else{
        //                     self.$message.error('数据加载失败:',res.data.errorMsg);
        //                     self.loading=false;
        //                 }
        //             }).catch(function (error) {
        //                 console.log(error);
        //                 self.loading=false;
        //             })
        //         }).catch(function (error){     
        //             console.log(error);   
        //     }); 
        // },
        // LoadApiData(apiId){//加载接口的数据
        //     let self = this;
        //     self.$axios.get('/api/ApiCaseMaintenance/LoadData',{
        //         params:{
        //           'apiId':apiId,
        //         }
        //     }).then(res => {
        //        if(res.data.statusCode==2000){
        //             self.EditCaseRomeData.requestType=res.data.apiInfo.requestType;
        //             self.EditCaseRomeData.requestUrl=res.data.apiInfo.requestUrl;
                
        //             //headers
        //             res.data.apiInfo.request.headers.forEach(item_headers=>{
        //                 if(self.EditCaseRomeData.tableData.length==0){
        //                     let obj = {};
        //                     obj.index = item_headers.index;
        //                     obj.state =item_headers.state;
        //                     obj.key =item_headers.key;
        //                     obj.value='';
        //                     obj.remarks=item_headers.remarks;

        //                     self.EditCaseRomeData.headersRomeData.tableData.push(obj);
        //                 }else{
        //                     self.EditCaseRomeData.tableData.forEach(d=>{
        //                         let tableData = d.headers.find(item=>
        //                             item.key == item_headers.key
        //                         );
        //                         if(tableData){

        //                         }else{
        //                             let obj = {};
        //                             obj.index = item_headers.index;
        //                             obj.state =item_headers.state;
        //                             obj.key =item_headers.key;
        //                             obj.value='';
        //                             obj.remarks=item_headers.remarks;

        //                             self.EditCaseRomeData.headersRomeData.tableData.push(obj);
        //                         }
        //                     });
        //                 }
        //             });
        //             self.EditCaseRomeData.headersRomeData.index= self.EditCaseRomeData.headersRomeData.tableData.length+1;

        //             //params
        //             res.data.apiInfo.request.params.forEach(item_params=>{
        //                 let obj = {};
        //                 obj.index = item_params.index;
        //                 obj.state =item_params.state;
        //                 obj.key =item_params.key;
        //                 obj.value='';
        //                 obj.remarks=item_params.remarks;
        //                 self.EditCaseRomeData.paramsRomeData.tableData.push(obj);
        //             });
        //             self.EditCaseRomeData.paramsRomeData.index=res.data.apiInfo.request.params.length+1;

        //             //body
        //             self.EditCaseRomeData.bodyRomeData.requestSaveType = res.data.apiInfo.request.body.requestSaveType;
        //             if(res.data.apiInfo.request.body.requestSaveType=='form-data'){
        //                 res.data.apiInfo.request.body.bodyData.forEach(item_body=>{
        //                     let obj = {};
        //                     obj.index = item_body.index;
        //                     obj.state =item_body.state;
        //                     obj.key =item_body.key;
        //                     obj.value='';
        //                     obj.remarks=item_body.remarks;
        //                     self.EditCaseRomeData.bodyRomeData.tableData.push(obj);
        //                 });
        //                 self.EditCaseRomeData.bodyRomeData.index=res.data.apiInfo.request.body.bodyData.length+1;
        //             }else if(res.data.apiInfo.request.body.requestSaveType=='raw'){
        //                 self.EditCaseRomeData.bodyRomeData.rawValue = res.data.apiInfo.request.body.bodyData;
        //             }               
        //        }else{
        //            self.$message.error('数据获取失败:',res.data.errorMsg);
        //        }
        //     }).catch(function (error) {
        //         console.log(error);
        //     })
        // },
        // SaveCurrentRomeData(){//因为切换接口的时候才会保存上一条数据,所以这里需要有1个专门的 保存当前数据的方法,上一步,下一步的时候把当前的数据保存进去
        //     let self = this;
        //     let tempCaseTable = self.EditCaseRomeData.tableData.find(item=>
        //         item.apiId == self.EditCaseRomeData.apiId
        //     );
        //     if(tempCaseTable){
        //         self.EditCaseRomeData.tableData.forEach((d,i)=>{
        //             if(d.apiId==self.EditCaseRomeData.apiId){
        //                 self.EditCaseRomeData.tableData[i].requestType =self.EditCaseRomeData.requestType;
        //                 self.EditCaseRomeData.tableData[i].requestUrl =self.EditCaseRomeData.requestUrl;
                        
        //                 self.EditCaseRomeData.tableData[i].headers =self.EditCaseRomeData.headersRomeData.tableData;
        //                 self.EditCaseRomeData.tableData[i].params =self.EditCaseRomeData.paramsRomeData.tableData;

        //                 self.EditCaseRomeData.tableData[i].body.requestSaveType =self.EditCaseRomeData.bodyRomeData.requestSaveType;
        //                 self.EditCaseRomeData.tableData[i].body.tableData =self.EditCaseRomeData.bodyRomeData.tableData;
        //                 self.EditCaseRomeData.tableData[i].body.rawValue =self.EditCaseRomeData.bodyRomeData.rawValue;

        //                 self.EditCaseRomeData.tableData[i].extract.tableData =self.EditCaseRomeData.extractRomeData.tableData;
        //                 self.EditCaseRomeData.tableData[i].validate.tableData =self.EditCaseRomeData.validateRomeData.tableData;

        //                 self.EditCaseRomeData.tableData[i].preOperation.tableData =self.EditCaseRomeData.preOperationRomeData.tableData;
        //                 self.EditCaseRomeData.tableData[i].rearOperation.tableData =self.EditCaseRomeData.rearOperationRomeData.tableData;
        //                 PrintConsole('覆盖数据id:',self.CaseRomeData.apiId)
        //             }
        //         });
        //     }else{
        //         let obj = {};
        //         obj.apiId = self.EditCaseRomeData.apiId;
        //         // obj.testName = testName;
        //         obj.requestType = self.EditCaseRomeData.requestType;
        //         obj.requestUrl = self.EditCaseRomeData.requestUrl;
        //         obj.headers = self.EditCaseRomeData.headersRomeData.tableData;
        //         obj.params = self.EditCaseRomeData.paramsRomeData.tableData;
        //         obj.body = {
        //             'tableData':self.EditCaseRomeData.bodyRomeData.tableData,
        //             'requestSaveType':self.EditCaseRomeData.bodyRomeData.requestSaveType,
        //             'rawValue':self.EditCaseRomeData.bodyRomeData.rawValue,
        //             }
        //         obj.extract = self.EditCaseRomeData.extractRomeData.tableData;
        //         obj.validate = self.EditCaseRomeData.validateRomeData.tableData;
        //         obj.preOperation = self.EditCaseRomeData.preOperationRomeData.tableData;
        //         obj.rearOperation = self.EditCaseRomeData.rearOperationRomeData.tableData;


        //         self.EditCaseRomeData.tableData.push(obj);
        //         PrintConsole('新增数据')
        //     }
        // },
        // UpdateTestNameToTable(){//更新测试名称和接口的状态到最终列表,在下一步的时候使用
        //     let self = this;
        //     self.TestSetRomeData.tableData.forEach(item=>{
        //         self.EditCaseRomeData.tableData.forEach((d,i)=>{
        //             if(d.apiId == item.id){
        //                 self.EditCaseRomeData.tableData[i].testName = item.testName;
        //                 self.EditCaseRomeData.tableData[i].state = item.state;
        //             }
        //         });
               
        //     });
        //     PrintConsole('更新测试名称');
        // },

        //headersRomeData
        
        
        CreateNewHeadersData(){
            let self = this;
            let obj = {};
            obj.index = self.EditCaseRomeData.headersRomeData.index;
            obj.state = true;
            obj.key = '';
            obj.value='';
            obj.remarks='';

            self.EditCaseRomeData.headersRomeData.tableData.push(obj);
            self.EditCaseRomeData.headersRomeData.index+=1;
        },
        handleHeadersDelete(index,row){
            PrintConsole('handleHeadersDelete',row);
            let self = this;
            self.EditCaseRomeData.headersRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.EditCaseRomeData.headersRomeData.tableData.forEach((item,i)=>{
                self.EditCaseRomeData.headersRomeData.tableData[i].index = i;
            });

            self.EditCaseRomeData.headersRomeData.index -=1 ;
        },
        cancelHeadersBulkEdit(){//批量修改模式下的取消
            this.EditCaseRomeData.headersRomeData.editModel='From';
            this.EditCaseRomeData.headersRomeData.showBulkEdit ='';
            this.EditCaseRomeData.headersRomeData.actualBulkEdit ='';
        },
        changesHeadersEditModel(){
            let self = this;
            if(self.EditCaseRomeData.headersRomeData.editModel=='From'){
                self.EditCaseRomeData.headersRomeData.editModel='Bulk';
                self.EditCaseRomeData.headersRomeData.bulkEdit ='';
                self.EditCaseRomeData.headersRomeData.tableData.forEach(item=>{
                    PrintConsole('changesHeadersBulkState',item);
                    let rowData=item.state+',';
                    if(item.key){
                        rowData+=item.key+',';
                    }else{
                        rowData+=',';
                    }
                    if(item.value){
                        rowData+=item.value+',';
                    }else{
                        rowData+=',';
                    }
                    if(item.remarks){
                        rowData+=item.remarks;
                    }
                    rowData+='\n';
                    self.EditCaseRomeData.headersRomeData.bulkEdit +=rowData;
                });
            }else{
                PrintConsole(self.EditCaseRomeData.headersRomeData.bulkEdit.split('\n'));

                self.EditCaseRomeData.headersRomeData.editModel='From';
                self.EditCaseRomeData.headersRomeData.tableData=[];
                self.EditCaseRomeData.headersRomeData.index = 0
                let bulkEdit = self.EditCaseRomeData.headersRomeData.bulkEdit.split('\n');
                bulkEdit.forEach(item=>{
                    if(item){
                        let data = item.split(',');

                        let obj = {};
                        obj.index = self.EditCaseRomeData.headersRomeData.index;
                        if(data[0]=="true"){
                            obj.state = true;
                        }else{
                            obj.state = false;
                        }
                        obj.key = data[1];
                        obj.value = data[2];
                        if(data.length==4){
                            obj.remarks = data[3];
                        }else{
                            obj.remarks ='';
                        }
                        // PrintConsole(obj);
                        self.EditCaseRomeData.headersRomeData.tableData.push(obj);
                    }
                });
                PrintConsole(self.EditCaseRomeData.headersRomeData.tableData);
            }
        },

        //paramsRomeData
        CreateNewParamsData(){
            let self = this;
            let obj = {};
            obj.index = self.EditCaseRomeData.paramsRomeData.index;
            obj.state = true;
            obj.key = '';
            obj.value='';
            obj.remarks='';

            self.EditCaseRomeData.paramsRomeData.tableData.push(obj);
            self.EditCaseRomeData.paramsRomeData.index+=1;
            PrintConsole('CreateNewParamsData',self.EditCaseRomeData.paramsRomeData.tableData);
        },
        handleParamsDelete(index,row){
            PrintConsole('handleParamsDelete',row);
            let self = this;
            self.EditCaseRomeData.paramsRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.EditCaseRomeData.paramsRomeData.tableData.forEach((item,i)=>{
                self.EditCaseRomeData.paramsRomeData.tableData[i].index = i;
            });

            self.EditCaseRomeData.paramsRomeData.index -=1 ;
        },
        cancelParamsBulkEdit(){//批量修改模式下的取消
            this.EditCaseRomeData.paramsRomeData.editModel='From';
            this.EditCaseRomeData.paramsRomeData.showBulkEdit ='';
            this.EditCaseRomeData.paramsRomeData.actualBulkEdit ='';
        },
        changesParamsEditModel(){
            let self = this;
            if(self.EditCaseRomeData.paramsRomeData.editModel=='From'){
                self.EditCaseRomeData.paramsRomeData.editModel='Bulk';
                self.EditCaseRomeData.paramsRomeData.bulkEdit ='';
                self.EditCaseRomeData.paramsRomeData.tableData.forEach(item=>{
                    PrintConsole('changesParamsEditModel',item);
                    let rowData=item.state+',';
                    if(item.key){
                        rowData+=item.key+',';
                    }else{
                        rowData+=',';
                    }
                    if(item.value){
                        rowData+=item.value+',';
                    }else{
                        rowData+=',';
                    }
                    if(item.remarks){
                        rowData+=item.remarks;
                    }
                    rowData+='\n';
                    self.EditCaseRomeData.paramsRomeData.bulkEdit +=rowData;
                });
            }else{
                PrintConsole(self.EditCaseRomeData.paramsRomeData.bulkEdit.split('\n'));

                self.EditCaseRomeData.paramsRomeData.editModel='From';
                self.EditCaseRomeData.paramsRomeData.tableData=[];
                self.EditCaseRomeData.paramsRomeData.index = 0
                let bulkEdit = self.EditCaseRomeData.paramsRomeData.bulkEdit.split('\n');
                bulkEdit.forEach(item=>{
                    if(item){
                        let data = item.split(',');

                        let obj = {};
                        obj.index = self.EditCaseRomeData.paramsRomeData.index;
                        if(data[0]=="true"){
                            obj.state = true;
                        }else{
                            obj.state = false;
                        }
                        obj.key = data[1];
                        obj.value = data[2];
                        if(data.length==4){
                            obj.remarks = data[3];
                        }else{
                            obj.remarks ='';
                        }
                        // PrintConsole(obj);
                        self.EditCaseRomeData.paramsRomeData.tableData.push(obj);
                    }
                });
                PrintConsole(self.EditCaseRomeData.paramsRomeData.tableData);
            }
        },

        //bodyRomeDta
        changeBodyRequestType(val){
            PrintConsole(val);
        },
        CreateNewBodyData(){
            let self = this;
            let obj = {};
            obj.index = self.EditCaseRomeData.bodyRomeData.index;
            obj.state = true;
            obj.key = '';
            obj.value='';
            obj.remarks='';

            self.EditCaseRomeData.bodyRomeData.tableData.push(obj);
            self.EditCaseRomeData.bodyRomeData.index+=1;
            PrintConsole('CreateNewBodyData',self.EditCaseRomeData.bodyRomeData.tableData);
        },
        handleBodyDelete(index,row){
            PrintConsole('handleBodyDelete',row);
            let self = this;
            self.EditCaseRomeData.bodyRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.EditCaseRomeData.bodyRomeData.tableData.forEach((item,i)=>{
                self.EditCaseRomeData.bodyRomeData.tableData[i].index = i;
            });

            self.EditCaseRomeData.bodyRomeData.index -=1 ;
        },
        cancelBodyBulkEdit(){//批量修改模式下的取消
            this.EditCaseRomeData.bodyRomeData.editModel='From';
            this.EditCaseRomeData.bodyRomeData.showBulkEdit ='';
            this.EditCaseRomeData.bodyRomeData.actualBulkEdit ='';
        },
        changesBodyEditModel(){
            let self = this;
            if(self.EditCaseRomeData.bodyRomeData.editModel=='From'){
                self.EditCaseRomeData.bodyRomeData.editModel='Bulk';
                self.EditCaseRomeData.bodyRomeData.bulkEdit ='';
                self.EditCaseRomeData.bodyRomeData.tableData.forEach(item=>{
                    PrintConsole('changesBodyEditModel',item);
                    let rowData=item.state+',';
                    if(item.key){
                        rowData+=item.key+',';
                    }else{
                        rowData+=',';
                    }
                    if(item.value){
                        rowData+=item.value+',';
                    }else{
                        rowData+=',';
                    }
                    if(item.remarks){
                        rowData+=item.remarks;
                    }
                    rowData+='\n';
                    self.EditCaseRomeData.bodyRomeData.bulkEdit +=rowData;
                });
            }else{
                PrintConsole(self.EditCaseRomeData.bodyRomeData.bulkEdit.split('\n'));

                self.EditCaseRomeData.bodyRomeData.editModel='From';
                self.EditCaseRomeData.bodyRomeData.tableData=[];
                self.EditCaseRomeData.bodyRomeData.index = 0
                let bulkEdit = self.EditCaseRomeData.bodyRomeData.bulkEdit.split('\n');
                bulkEdit.forEach(item=>{
                    if(item){
                        let data = item.split(',');

                        let obj = {};
                        obj.index = self.EditCaseRomeData.bodyRomeData.index;
                        if(data[0]=="true"){
                            obj.state = true;
                        }else{
                            obj.state = false;
                        }
                        obj.key = data[1];
                        obj.value = data[2];
                        if(data.length==4){
                            obj.remarks = data[3];
                        }else{
                            obj.remarks ='';
                        }
                        // PrintConsole(obj);
                        self.EditCaseRomeData.bodyRomeData.tableData.push(obj);
                    }
                });
                PrintConsole(self.EditCaseRomeData.bodyRomeData.tableData);
            }
        },

        //extractRomeData
        CreateNewExtractData(){
            let self = this;
            let obj = {};
            obj.index = self.EditCaseRomeData.extractRomeData.index;
            obj.state = true;
            obj.key = '';
            obj.value='';
            obj.remarks='';

            self.EditCaseRomeData.extractRomeData.tableData.push(obj);
            self.EditCaseRomeData.extractRomeData.index+=1;
            PrintConsole('CreateNewExtractData',self.EditCaseRomeData.extractRomeData.tableData);
        },
        handleExtractDelete(index,row){
            PrintConsole('handleExtractDelete',row);
            let self = this;
            self.EditCaseRomeData.extractRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.EditCaseRomeData.extractRomeData.tableData.forEach((item,i)=>{
                self.EditCaseRomeData.extractRomeData.tableData[i].index = i;
            });
            self.EditCaseRomeData.extractRomeData.index -=1 ;
        },

        //validateRomeData
        GetExtractKeyName(){//获取提取中的key值
            let self = this;
            let checkOptions = [];
            self.EditCaseRomeData.extractRomeData.tableData.forEach(e =>{
                if(e.state){
                    let obj ={};
                    obj.label = e.key;
                    obj.value = e.key;
                    checkOptions.push(obj);
                }
            })
            PrintConsole('GetExtractKeyName',checkOptions);
            return checkOptions
        },
        createFilterValidate(queryString) {
            return (restaurant) => {
                return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
            };
        },
        fetchSuggestionsValidate(queryString, cb){//断言点击输入框会加载断言的数据
            var restaurants = this.GetExtractKeyName();
            var results = queryString ? restaurants.filter(this.createFilterValidate(queryString)) : restaurants;
            // 调用 callback 返回建议列表的数据
            cb(results);
        },
        CreateNewValidateData(){
            let self = this;
            let obj = {};
            obj.index = self.EditCaseRomeData.validateRomeData.index;
            obj.state = true;
            obj.checkName = '';
            obj.validateType='';
            obj.valueType='';//断言值类型
            obj.expectedResults='';
            obj.remarks='';

            self.EditCaseRomeData.validateRomeData.tableData.push(obj);
            self.EditCaseRomeData.validateRomeData.index+=1;
            PrintConsole('CreateNewValidateData',self.EditCaseRomeData.validateRomeData.tableData);
        },
        handleValidateDelete(index,row){
            PrintConsole('handleValidateDelete',row);
            let self = this;
            self.EditCaseRomeData.validateRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.EditCaseRomeData.validateRomeData.tableData.forEach((item,i)=>{
                self.EditCaseRomeData.validateRomeData.tableData[i].index = i;
            });
            self.EditCaseRomeData.validateRomeData.index -=1 ;
        },

        //前置操作
        handlePreOperationCommand(command){
            PrintConsole('handlePreOperationCommand:',command);
            this.CreateNewPreOperationData(command);
        },
        CreateNewPreOperationData(operationType){
            let self = this;
            let obj = {};
            obj.id = self.EditCaseRomeData.preOperationRomeData.index;
            obj.index = self.EditCaseRomeData.preOperationRomeData.index;
            obj.state = true;
            obj.operationType = operationType;
            obj.methodsName='';
            obj.dataBase='';
            obj.sql='';

            obj.remarks='';

            self.EditCaseRomeData.preOperationRomeData.tableData.push(obj);
            self.EditCaseRomeData.preOperationRomeData.index+=1;
            self.rowDropPreOperation();
            PrintConsole('CreateNewMethodsData',self.EditCaseRomeData.preOperationRomeData.tableData);
        },
        handlePreOperationDelete(index,row){
            PrintConsole('handlePreOperationDelete',row);
            let self = this;
            self.EditCaseRomeData.preOperationRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.EditCaseRomeData.preOperationRomeData.tableData.forEach((item,i)=>{
                self.EditCaseRomeData.preOperationRomeData.tableData[i].index = i;
            });
            self.EditCaseRomeData.preOperationRomeData.index -=1 ;
        },
        rowDropPreOperation() {//加载可拖动效果
            PrintConsole('加载可拖动效果')
            const tbody = document.querySelector('#PreOperationSort > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(2)');
            let self = this;
            Sortable.create(tbody, {
                onEnd ({ newIndex, oldIndex }) {
                    const currRow = self.EditCaseRomeData.preOperationRomeData.tableData.splice(oldIndex, 1)[0];
                    self.EditCaseRomeData.preOperationRomeData.tableData.splice(newIndex, 0, currRow);
                    self.SortPreOperation();
                }
            });
        },
        SortPreOperation(){//调用 每次拖动完成后调用重新排序
            let self = this;
            self.EditCaseRomeData.preOperationRomeData.tableData.forEach((d,index)=>{
                self.EditCaseRomeData.preOperationRomeData.tableData[index].rowNum = index;
            });
            PrintConsole('SortPreOperation:重新排序',self.EditCaseRomeData.preOperationRomeData.tableData);
        },

        //后置操作
        handleRearOperationCommand(command){
            PrintConsole('handleRearOperationCommand:',command);
            this.CreateNewRearOperationData(command);
        },
        CreateNewRearOperationData(operationType){
            let self = this;
            let obj = {};
            obj.id = self.EditCaseRomeData.rearOperationRomeData.index;
            obj.index = self.EditCaseRomeData.rearOperationRomeData.index;
            obj.state = true;
            obj.operationType = operationType;
            obj.methodsName='';
            obj.dataBase='';
            obj.sql='';

            obj.remarks='';

            self.EditCaseRomeData.rearOperationRomeData.tableData.push(obj);
            self.EditCaseRomeData.rearOperationRomeData.index+=1;
            self.rowDropRearOperation();
            PrintConsole('CreateNewRearOperationData',self.EditCaseRomeData.rearOperationRomeData.tableData);
        },
        handleRearOperationDelete(index,row){
            PrintConsole('handleRearOperationDelete',row);
            let self = this;
            self.EditCaseRomeData.rearOperationRomeData.tableData.splice(index, 1)//删除列表中的数据
        
            self.EditCaseRomeData.rearOperationRomeData.tableData.forEach((item,i)=>{
                self.EditCaseRomeData.rearOperationRomeData.tableData[i].index = i;
            });
            self.EditCaseRomeData.rearOperationRomeData.index -=1 ;
        },
        rowDropRearOperation() {//加载可拖动效果
            PrintConsole('加载可拖动效果')
            const tbody = document.querySelector('#RearOperationSort > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(2)');
            let self = this;
            Sortable.create(tbody, {
                onEnd ({ newIndex, oldIndex }) {
                    const currRow = self.EditCaseRomeData.rearOperationRomeData.tableData.splice(oldIndex, 1)[0];
                    self.EditCaseRomeData.rearOperationRomeData.tableData.splice(newIndex, 0, currRow);
                    self.SortRearOperation();
                }
            });
        },
        SortRearOperation(){//调用 每次拖动完成后调用重新排序
            let self = this;
            self.EditCaseRomeData.rearOperationRomeData.tableData.forEach((d,index)=>{
                self.EditCaseRomeData.rearOperationRomeData.tableData[index].rowNum = index;
            });
            PrintConsole('SortRearOperation:重新排序',self.EditCaseRomeData.rearOperationRomeData.tableData);
        },
    }
};
</script>

<style>
.table {display: table; width: 100%;}
.father {display: table-cell; vertical-align: middle;}
.son {margin: auto;}
.bodyRome{
    margin-top:10px;
}
</style>
