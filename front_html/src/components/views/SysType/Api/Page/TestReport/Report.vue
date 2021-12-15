<template>
    <div ref="tab-main"  id="tab-main">
        <template>
            <div ref="tab-second" class="flex-layout" id="tab-second">
                <el-row>
                    <el-col :span="10">
                        <el-row class="TopTitle">
                            <el-col :span="24">
                                <h1>{{RomeData.TopData.reportName}}</h1>
                            </el-col>
                            <el-col :span="24">
                                <div class="TopMargin">
                                    <strong>创建时间:</strong>
                                    <el-tag>{{RomeData.TopData.createTime}}</el-tag>
                                </div>
                            </el-col>
                            <el-col :span="24">
                                <div class="TopMargin">
                                    <strong>耗时时长:</strong>
                                    <el-tag type="success">{{RomeData.TopData.runningTime}}</el-tag>
                                </div>
                            </el-col>
                            <el-col :span="24">
                                <div class="TopMargin">
                                    <strong>测试统计:</strong>
                                    <el-tag type="success">成功:{{RomeData.TopData.passTotal}}</el-tag>&nbsp;&nbsp;
                                    <el-tag type="warning">失败:{{RomeData.TopData.failTotal}}</el-tag>&nbsp;&nbsp;
                                    <el-tag type="danger">错误:{{RomeData.TopData.errorTotal}}</el-tag>&nbsp;
                                </div>
                            </el-col>
                            <el-col :span="24">
                                <div class="TopMargin">
                                    <strong>测试结果:</strong>
                                    <el-tag v-if="RomeData.TopData.reportStatus=='Pass'" type="success">通过</el-tag>
                                    <el-tag v-else type="warning">未通过</el-tag>
                                </div>
                            </el-col>
                        </el-row>
                    </el-col>
                    <el-card shadow="never" style="height:250px">
                        <el-col :span="7">
                            <div style="margin-top:-10px" id="EchartContainer-bar" class="EchartContainer-bar"></div>   
                        </el-col>
                        <el-col :span="7">
                            <div style="margin-top:-55px;margin-left:200px" id="EchartContainer-pie" class="EchartContainer-pie"></div>   
                        </el-col>
                    </el-card>
                </el-row>
                <div style="margin-top:-10px">
                    <el-divider></el-divider>
                </div>
                <div style="margin-top:-15px">
                    <template>
                        <el-tabs tab-position="left" @tab-click="handleClick_firstMenu"> 
                            <el-tab-pane  v-for="pane in RomeData.firstMenu" :key="pane.id" :label="pane.label" :name="pane.name">
                                <div v-if="reportType=='API' || reportType=='CASE'">
                                    <el-collapse>
                                        <div>
                                            <template>
                                                <el-tabs v-model="RomeData.activeName">
                                                    <!-- <el-tab-pane label="Headers" name="Headers">
                                                        <div>
                                                            <el-table
                                                            :data="NewRomeData.GeneralTableData"
                                                            style="width: 1000px">
                                                            <el-table-column
                                                                prop="key"
                                                                label="General"
                                                                width="180">
                                                            </el-table-column>
                                                            <el-table-column>
                                                                <template slot-scope="scope">
                                                                    <div v-if="scope.row.key=='Status Code:'">
                                                                        <el-tag v-if="scope.row.value==200" type="success">{{scope.row.value}}</el-tag>
                                                                        <el-tag v-else type="danger">{{scope.row.value}}</el-tag>
                                                                    </div>
                                                                    <div v-else>
                                                                        <span>{{scope.row.value}}</span>
                                                                    </div>
                                                                </template>
                                                            </el-table-column>
                                                            </el-table>
                                                        </div>
                                                        <div>
                                                            <el-table
                                                            :data="NewRomeData.RequestHeaders" 
                                                            style="width: 1000px">
                                                            <el-table-column
                                                                prop="key"
                                                                label="Request Headers"
                                                                width="180">
                                                            </el-table-column>
                                                            <el-table-column>
                                                                <template slot-scope="scope">
                                                                    <div v-if="scope.row.key=='Status Code:'">
                                                                        <el-tag v-if="scope.row.value==200" type="success">{{scope.row.value}}</el-tag>
                                                                        <el-tag v-else type="danger">{{scope.row.value}}</el-tag>
                                                                    </div>
                                                                    <div v-else>
                                                                        <span>{{scope.row.value}}</span>
                                                                    </div>
                                                                </template>
                                                            </el-table-column>
                                                            </el-table>
                                                        </div>
                                                        <div v-if="NewRomeData.RequestData.length!=0">
                                                            <el-table
                                                            :data="NewRomeData.RequestData"
                                                            style="width: 1000px">
                                                            <el-table-column
                                                                prop="key"
                                                                label="Request Parameters"
                                                                width="180">
                                                            </el-table-column>
                                                            <el-table-column
                                                                prop="value">
                                                            </el-table-column>
                                                            </el-table>
                                                        </div>
                                                        <div v-if="NewRomeData.RequestFile.length!=0">
                                                            <el-table
                                                            :data="NewRomeData.RequestFile"
                                                            style="width: 1000px">
                                                            <el-table-column
                                                                prop="key"
                                                                label="Request File"
                                                                width="180">
                                                            </el-table-column>
                                                            <el-table-column
                                                                prop="value">
                                                            </el-table-column>
                                                            </el-table>
                                                        </div>
                                                    </el-tab-pane>
                                                    <el-tab-pane label="Response" name="Response">
                                                        <el-input type="textarea" 
                                                            readonly
                                                            resize="none"
                                                            v-model="NewRomeData.responseData"
                                                            :autosize="{ minRows: 25, maxRows: 25}"
                                                            >
                                                        </el-input>
                                                    </el-tab-pane>
                                                    <el-tab-pane label="Test Results" name="Results" v-if="NewRomeData.TestResults.extractTabelData.length!=0">
                                                        <div>
                                                            <el-table
                                                            :data="NewRomeData.TestResults.extractTabelData"
                                                            style="width: 1000px">
                                                            <el-table-column
                                                                prop="key"
                                                                label="Extract(提取)"
                                                                width="180">
                                                            </el-table-column>
                                                            <el-table-column
                                                                prop="value">
                                                            </el-table-column>
                                                            </el-table>
                                                        </div>
                                                        <el-divider></el-divider>
                                                        <div>
                                                            <el-table
                                                            :data="NewRomeData.TestResults.validateResults"
                                                            style="width: 1000px">
                                                            <el-table-column label="Valdate Results"  align="center">
                                                                <el-table-column
                                                                    align="center"
                                                                    prop="check"
                                                                    label="检查值"
                                                                    width="180">
                                                                </el-table-column>
                                                            </el-table-column>
                                                            <el-table-column
                                                                align="center"
                                                                label="期望结果"
                                                                prop="retChecktext">
                                                            </el-table-column>
                                                            <el-table-column
                                                                align="center"
                                                                label="检查类型"
                                                                prop="comparator">
                                                            </el-table-column>
                                                            <el-table-column
                                                                align="center"
                                                                label="实际结果"
                                                                prop="retExtracttext">
                                                            </el-table-column>
                                                            <el-table-column
                                                                align="center"
                                                                label="测试结果">
                                                                <template slot-scope="scope">
                                                                    <el-tag type="success" v-if="scope.row.results">通过</el-tag>
                                                                    <el-tag type="warning" v-else>失败</el-tag>
                                                                </template>
                                                            </el-table-column>
                                                            </el-table>
                                                        </div>
                                                    </el-tab-pane>
                                                    <el-tab-pane label="Methods" name="Methods" v-if="NewRomeData.TestResults.methodsTabelData.length!=0">
                                                        <div>
                                                            <el-table
                                                            :data="NewRomeData.TestResults.methodsTabelData"
                                                            style="width: 1000px">
                                                            <el-table-column
                                                                align="center"
                                                                label="方法类型"
                                                                width="150px">
                                                                <template slot-scope="scope">
                                                                    <el-tag type="success" v-if="scope.row.methodsType=='Front'">前置操作</el-tag>
                                                                    <el-tag type="danger" v-else>后置操作</el-tag>
                                                                </template>
                                                            </el-table-column>
                                                            <el-table-column
                                                                align="center"
                                                                label="调用方法"
                                                                prop="methodsName">
                                                            </el-table-column>
                                                            <el-table-column
                                                                align="center"
                                                                label="说明"
                                                                prop="remarks">
                                                            </el-table-column>
                                                            <el-table-column
                                                                align="center"
                                                                label="执行结果"
                                                                prop="methodsResults">
                                                            </el-table-column>
                                                            </el-table>
                                                        </div>
                                                    </el-tab-pane>
                                                    <el-tab-pane label="ErrorMsg" name="ErrorMsg" v-if="NewRomeData.errorMsg">
                                                        <el-input type="textarea" 
                                                            readonly
                                                            resize="none"
                                                            v-model="NewRomeData.errorMsg"
                                                            :autosize="{ minRows: 25, maxRows: 25}">
                                                        </el-input>
                                                    </el-tab-pane> -->
                                                </el-tabs>
                                            </template>
                                        </div>
                                    </el-collapse>
                                </div>
                                <!-- <div v-else-if="reportType=='Task'">
                                    <el-tabs tab-position="left" @tab-click="handleClick_secondMenu"> 
                                        <el-tab-pane  v-for="pane in NewRomeData.secondMenu" :key="pane.id" :label="pane.label" :name="pane.name" v-loading="loading">
                                            <el-collapse>
                                                <div v-loading="loading">
                                                    <template>
                                                        <el-tabs v-model="NewRomeData.activeName">
                                                            <el-tab-pane label="Headers" name="Headers">
                                                                <div>
                                                                    <el-table
                                                                    :data="NewRomeData.GeneralTableData"
                                                                    style="width: 1000px">
                                                                    <el-table-column
                                                                        prop="key"
                                                                        label="General"
                                                                        width="180">
                                                                    </el-table-column>
                                                                    <el-table-column>
                                                                        <template slot-scope="scope">
                                                                            <div v-if="scope.row.key=='Status Code:'">
                                                                                <el-tag v-if="scope.row.value==200" type="success">{{scope.row.value}}</el-tag>
                                                                                <el-tag v-else type="danger">{{scope.row.value}}</el-tag>
                                                                            </div>
                                                                            <div v-else>
                                                                                <span>{{scope.row.value}}</span>
                                                                            </div>
                                                                        </template>
                                                                    </el-table-column>
                                                                    </el-table>
                                                                </div>
                                                                <div>
                                                                    <el-table
                                                                    :data="NewRomeData.RequestHeaders" 
                                                                    style="width: 1000px">
                                                                    <el-table-column
                                                                        prop="key"
                                                                        label="Request Headers"
                                                                        width="180">
                                                                    </el-table-column>
                                                                    <el-table-column>
                                                                        <template slot-scope="scope">
                                                                            <div v-if="scope.row.key=='Status Code:'">
                                                                                <el-tag v-if="scope.row.value==200" type="success">{{scope.row.value}}</el-tag>
                                                                                <el-tag v-else type="danger">{{scope.row.value}}</el-tag>
                                                                            </div>
                                                                            <div v-else>
                                                                                <span>{{scope.row.value}}</span>
                                                                            </div>
                                                                        </template>
                                                                    </el-table-column>
                                                                    </el-table>
                                                                </div>
                                                                <div v-if="NewRomeData.RequestData.length!=0">
                                                                    <el-table
                                                                    :data="NewRomeData.RequestData"
                                                                    style="width: 1000px">
                                                                    <el-table-column
                                                                        prop="key"
                                                                        label="Request Parameters"
                                                                        width="180">
                                                                    </el-table-column>
                                                                    <el-table-column
                                                                        prop="value">
                                                                    </el-table-column>
                                                                    </el-table>
                                                                </div>
                                                                <div v-if="NewRomeData.RequestFile.length!=0">
                                                                    <el-table
                                                                    :data="NewRomeData.RequestFile"
                                                                    style="width: 1000px">
                                                                    <el-table-column
                                                                        prop="key"
                                                                        label="Request File"
                                                                        width="180">
                                                                    </el-table-column>
                                                                    <el-table-column
                                                                        prop="value">
                                                                    </el-table-column>
                                                                    </el-table>
                                                                </div>
                                                            </el-tab-pane>
                                                            <el-tab-pane label="Response" name="Response">
                                                                <el-input type="textarea" 
                                                                    readonly
                                                                    resize="none"
                                                                    v-model="NewRomeData.responseData"
                                                                    :autosize="{ minRows: 25, maxRows: 25}"
                                                                    >
                                                                </el-input>
                                                            </el-tab-pane>
                                                            <el-tab-pane label="Test Results" name="Results" v-if="NewRomeData.TestResults.extractTabelData.length!=0">
                                                                <div>
                                                                    <el-table
                                                                    :data="NewRomeData.TestResults.extractTabelData">
                                                                    <el-table-column
                                                                        prop="key"
                                                                        label="Extract(提取)"
                                                                        width="180">
                                                                    </el-table-column>
                                                                    <el-table-column
                                                                        prop="value">
                                                                    </el-table-column>
                                                                    </el-table>
                                                                </div>
                                                                <el-divider></el-divider>
                                                                <div>
                                                                    <el-table
                                                                    :data="NewRomeData.TestResults.validateResults">
                                                                    <el-table-column label="Valdate Results"  align="center">
                                                                        <el-table-column
                                                                            align="center"
                                                                            prop="check"
                                                                            label="检查值"
                                                                            width="180">
                                                                        </el-table-column>
                                                                    </el-table-column>
                                                                    <el-table-column
                                                                        show-overflow-tooltip
                                                                        align="center"
                                                                        label="期望结果"
                                                                        prop="retChecktext">
                                                                    </el-table-column>
                                                                    <el-table-column
                                                                        align="center"
                                                                        label="检查类型"
                                                                        prop="comparator">
                                                                    </el-table-column>
                                                                    <el-table-column
                                                                        show-overflow-tooltip
                                                                        align="center"
                                                                        label="实际结果"
                                                                        prop="retExtracttext">
                                                                    </el-table-column>
                                                                    <el-table-column
                                                                        align="center"
                                                                        label="测试结果">
                                                                        <template slot-scope="scope">
                                                                            <el-tag type="success" v-if="scope.row.results">通过</el-tag>
                                                                            <el-tag type="warning" v-else>失败</el-tag>
                                                                        </template>
                                                                    </el-table-column>
                                                                    </el-table>
                                                                </div>
                                                            </el-tab-pane>
                                                            <el-tab-pane label="Methods" name="Methods" v-if="NewRomeData.TestResults.methodsTabelData.length!=0">
                                                                <div>
                                                                    <el-table
                                                                    :data="NewRomeData.TestResults.methodsTabelData"
                                                                    style="width: 1000px">
                                                                    <el-table-column
                                                                        align="center"
                                                                        label="方法类型"
                                                                        width="150px">
                                                                        <template slot-scope="scope">
                                                                            <el-tag type="success" v-if="scope.row.methodsType=='Front'">前置操作</el-tag>
                                                                            <el-tag type="danger" v-else>后置操作</el-tag>
                                                                        </template>
                                                                    </el-table-column>
                                                                    <el-table-column
                                                                        align="center"
                                                                        label="调用方法"
                                                                        prop="methodsName">
                                                                    </el-table-column>
                                                                    <el-table-column
                                                                        align="center"
                                                                        label="说明"
                                                                        prop="remarks">
                                                                    </el-table-column>
                                                                    <el-table-column
                                                                        align="center"
                                                                        label="执行结果"
                                                                        prop="methodsResults">
                                                                    </el-table-column>
                                                                    </el-table>
                                                                </div>
                                                            </el-tab-pane>
                                                            <el-tab-pane label="ErrorMsg" name="ErrorMsg" v-if="NewRomeData.errorMsg">
                                                                <el-input type="textarea" 
                                                                    readonly
                                                                    resize="none"
                                                                    v-model="NewRomeData.errorMsg"
                                                                    :autosize="{ minRows: 25, maxRows: 25}">
                                                                </el-input>
                                                            </el-tab-pane>
                                                        </el-tabs>
                                                    </template>
                                                </div>
                                            </el-collapse>
                                        </el-tab-pane>
                                    </el-tabs>
                                </div>
                                <div v-else>
                                    <el-tabs tab-position="left" @tab-click="handleClick_secondMenu"> 
                                        <el-tab-pane  v-for="pane in NewRomeData.secondMenu" :key="pane.id" :label="pane.label" :name="pane.name" v-loading="loading">
                                            <el-tabs tab-position="left" @tab-click="handleClick_thirdMenu"> 
                                                <el-tab-pane  v-for="pane in NewRomeData.thirdMenu" :key="pane.id" :label="pane.label" :name="pane.name" v-loading="loading">
                                                    <div v-loading="loading">
                                                        <template>
                                                            <el-tabs v-model="NewRomeData.activeName">
                                                                <el-tab-pane label="Headers" name="Headers">
                                                                    <div>
                                                                        <el-table
                                                                        :data="NewRomeData.GeneralTableData">
                                                                        <el-table-column
                                                                            prop="key"
                                                                            label="General"
                                                                            width="180">
                                                                        </el-table-column>
                                                                        <el-table-column>
                                                                            <template slot-scope="scope">
                                                                                <div v-if="scope.row.key=='Status Code:'">
                                                                                    <el-tag v-if="scope.row.value==200" type="success">{{scope.row.value}}</el-tag>
                                                                                    <el-tag v-else type="danger">{{scope.row.value}}</el-tag>
                                                                                </div>
                                                                                <div v-else>
                                                                                    <span>{{scope.row.value}}</span>
                                                                                </div>
                                                                            </template>
                                                                        </el-table-column>
                                                                        </el-table>
                                                                    </div>
                                                                    <div v-if="NewRomeData.RequestHeaders.length!=0">
                                                                        <el-table
                                                                        :data="NewRomeData.RequestHeaders" 
                                                                        style="width: 1000px">
                                                                        <el-table-column
                                                                            prop="key"
                                                                            label="Request Headers"
                                                                            width="180">
                                                                        </el-table-column>
                                                                        <el-table-column>
                                                                            <template slot-scope="scope">
                                                                                <div v-if="scope.row.key=='Status Code:'">
                                                                                    <el-tag v-if="scope.row.value==200" type="success">{{scope.row.value}}</el-tag>
                                                                                    <el-tag v-else type="danger">{{scope.row.value}}</el-tag>
                                                                                </div>
                                                                                <div v-else>
                                                                                    <span>{{scope.row.value}}</span>
                                                                                </div>
                                                                            </template>
                                                                        </el-table-column>
                                                                        </el-table>
                                                                    </div>
                                                                    <div v-if="NewRomeData.RequestData.length!=0">
                                                                        <el-table
                                                                        :data="NewRomeData.RequestData"
                                                                        style="width: 1000px">
                                                                        <el-table-column
                                                                            prop="key"
                                                                            label="Request Parameters"
                                                                            width="180">
                                                                        </el-table-column>
                                                                        <el-table-column
                                                                            prop="value">
                                                                        </el-table-column>
                                                                        </el-table>
                                                                    </div>
                                                                    <div v-if="NewRomeData.RequestFile.length!=0">
                                                                        <el-table
                                                                        :data="NewRomeData.RequestFile"
                                                                        style="width: 1000px">
                                                                        <el-table-column
                                                                            prop="key"
                                                                            label="Request File"
                                                                            width="180">
                                                                        </el-table-column>
                                                                        <el-table-column
                                                                            prop="value">
                                                                        </el-table-column>
                                                                        </el-table>
                                                                    </div>
                                                                </el-tab-pane>
                                                                <el-tab-pane label="Response" name="Response">
                                                                    <el-input type="textarea" 
                                                                        readonly
                                                                        resize="none"
                                                                        v-model="NewRomeData.responseData"
                                                                        :autosize="{ minRows: 25, maxRows: 25}"
                                                                        >
                                                                    </el-input>
                                                                </el-tab-pane>
                                                                <el-tab-pane label="Test Results" name="Results" v-if="NewRomeData.TestResults.extractTabelData.length!=0">
                                                                    <div>
                                                                        <el-table
                                                                        :data="NewRomeData.TestResults.extractTabelData">
                                                                        <el-table-column
                                                                            prop="key"
                                                                            label="Extract(提取)"
                                                                            width="180">
                                                                        </el-table-column>
                                                                        <el-table-column
                                                                            prop="value">
                                                                        </el-table-column>
                                                                        </el-table>
                                                                    </div>
                                                                    <el-divider></el-divider>
                                                                    <div>
                                                                        <el-table
                                                                        :data="NewRomeData.TestResults.validateResults">
                                                                        <el-table-column label="Valdate Results"  align="center">
                                                                            <el-table-column
                                                                                align="center"
                                                                                prop="check"
                                                                                label="检查值"
                                                                                width="180">
                                                                            </el-table-column>
                                                                        </el-table-column>
                                                                        <el-table-column
                                                                            show-overflow-tooltip
                                                                            align="center"
                                                                            label="期望结果"
                                                                            prop="retChecktext">
                                                                        </el-table-column>
                                                                        <el-table-column
                                                                            align="center"
                                                                            label="检查类型"
                                                                            prop="comparator">
                                                                        </el-table-column>
                                                                        <el-table-column
                                                                            show-overflow-tooltip
                                                                            align="center"
                                                                            label="实际结果"
                                                                            prop="retExtracttext">
                                                                        </el-table-column>
                                                                        <el-table-column
                                                                            align="center"
                                                                            label="测试结果">
                                                                            <template slot-scope="scope">
                                                                                <el-tag type="success" v-if="scope.row.results">通过</el-tag>
                                                                                <el-tag type="warning" v-else>失败</el-tag>
                                                                            </template>
                                                                        </el-table-column>
                                                                        </el-table>
                                                                    </div>
                                                                </el-tab-pane>
                                                                <el-tab-pane label="Methods" name="Methods" v-if="NewRomeData.TestResults.methodsTabelData.length!=0">
                                                                    <div>
                                                                        <el-table
                                                                        :data="NewRomeData.TestResults.methodsTabelData"
                                                                        style="width: 1000px">
                                                                        <el-table-column
                                                                            align="center"
                                                                            label="方法类型"
                                                                            width="150px">
                                                                            <template slot-scope="scope">
                                                                                <el-tag type="success" v-if="scope.row.methodsType=='Front'">前置操作</el-tag>
                                                                                <el-tag type="danger" v-else>后置操作</el-tag>
                                                                            </template>
                                                                        </el-table-column>
                                                                        <el-table-column
                                                                            align="center"
                                                                            label="调用方法"
                                                                            prop="methodsName">
                                                                        </el-table-column>
                                                                        <el-table-column
                                                                            align="center"
                                                                            label="说明"
                                                                            prop="remarks">
                                                                        </el-table-column>
                                                                        <el-table-column
                                                                            align="center"
                                                                            label="执行结果"
                                                                            prop="methodsResults">
                                                                        </el-table-column>
                                                                        </el-table>
                                                                    </div>
                                                                </el-tab-pane>
                                                                <el-tab-pane label="ErrorMsg" name="ErrorMsg" v-if="NewRomeData.errorMsg">
                                                                    <el-input type="textarea" 
                                                                        readonly
                                                                        resize="none"
                                                                        v-model="NewRomeData.errorMsg"
                                                                        :autosize="{ minRows: 25, maxRows: 25}">
                                                                    </el-input>
                                                                </el-tab-pane>
                                                            </el-tabs>
                                                        </template>
                                                    </div>
                                                </el-tab-pane>
                                            </el-tabs>
                                        </el-tab-pane>
                                    </el-tabs>
                                </div> -->
                            </el-tab-pane>
                        </el-tabs>
                    </template>
                </div>
            </div>
        </template>
    </div>
</template>

<script>
import * as echarts from 'echarts';
import {PrintConsole} from "../../../../../js/Logger.js";
export default {
    data() {
        return {
            loading:false,
            RomeData:{
                testReportId:'',
                TopData:{//头部数据
                    reportName:'',//报告标题
                    createTime:'',//开始时间
                    runningTime:'',//运行时长
                    passTotal:'',//成功数
                    failTotal:'',//失败数
                    errorTotal:'',//错误数
                    passRate:0,//通过率
                },
                activeName:'Headers',
                firstMenu:[],//1级菜单列表
                secondMenu:[],//2级菜单列表
                thirdMenu:[],//3级菜单列表
            }
        };
    },
    mounted(){
        PrintConsole('query',this.$route.query);
        this.RomeData.testReportId = this.$route.query.testReportId;
        this.loadReportData(this.RomeData.testReportId);
        // this.BarChart();
        // this.PieChart();


    },
    methods: {
        BarChart(){
            let self = this;
            var MyChart_bar = echarts.init(document.getElementById('EchartContainer-bar'));//初始化
            var option = {//设置各属性和数据
                title: {
                    show: true, //显示折线图
                    //   text: '各应用折线图:', //标题文字
                    left: 50, //配置title的位置
                    top:-10,
                    padding: [20,20,5,10] //title的padding值
                },
                tooltip: {
                    trigger: 'axis' //通过哪种方式触发tip
                },
                //图例，选择要显示的项目
                legend:{
                    left:'center',
                    data:['Pass','Fail','Error']//注意要和数据的name相对应
                },
                xAxis: {
                    type:'category',
                    data: ['本次执行接口步骤统计'],
                },
                yAxis: {
                    type: 'value',
                    axisLabel: {  
                        show: true,  
                        interval: 'auto',  
                        formatter: '{value}'  
                    },  
                    // splitLine: {//y轴横线图
                    //     show: true
                    // }
                },
                series: [
                    {"name": 'Pass',"data": [self.RomeData.TopData.passTotal],"type": 'bar',"itemStyle": {
                        "normal": {"color": '#91cc75'}}, 
                        "label": {'normal': {'show': 'true', 'position': 'top'}}
                    },
                    {"name": 'Fail',"data": [self.RomeData.TopData.failTotal],"type": 'bar',"itemStyle": {
                        "normal": {"color": '#fac858'}}, 
                        "label": {'normal': {'show': 'true', 'position': 'top'}}
                    },
                    {"name": 'Error',"data": [self.RomeData.TopData.errorTotal],"type": 'bar',"itemStyle": {
                        "normal": {"color": '#ee6666'}}, 
                        "label": {'normal': {'show': 'true', 'position': 'top'}}
                    },

                ]
            };
            MyChart_bar.setOption(option,true);//加载属性后显示 true自动每次清除数据
        },
        PieChart(passRate){
            let self = this;
            var MyChart_pie = echarts.init(document.getElementById('EchartContainer-pie'));//初始化
            var option = {//设置各属性和数据
                tooltip: {
                    trigger: 'item', //通过哪种方式触发tip
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                series:[{
                        name: '测试统计',
                        type: 'pie',
                        radius: ['40%', '70%'],
                        center: ['50%', '60%'],//好像是位置
                        label:{//中间文字配置
                            normal:{
                                show:true,
                                position:'center',
                                // color:'#9A9EBA',
                                fontSize:'17px',
                                formatter:'通过率\n'+passRate+'%',
                                emphasis:{//中间文字显示
                                    show:true
                                }
                            }
                        },
                        data:[
                            {"value": self.RomeData.TopData.passTotal, "name": 'Pass', "itemStyle": {"normal": {"color": '#91cc75'}}},
                            {"value": self.RomeData.TopData.failTotal, "name": 'Fail', "itemStyle": {"normal": {"color": '#fac858'}}},
                            {"value": self.RomeData.TopData.errorTotal, "name": 'Error', "itemStyle": {"normal": {"color": '#ee6666'}}},
                        ],
                        itemStyle: {
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }] 
            };
            MyChart_pie.setOption(option,true);//加载属性后显示 true自动每次清除数据
        },
        handleClick_firstMenu(tab, event){//点击1级名称加载2层数据
            PrintConsole(tab, event);
        },
        loadReportData(testReportId){
            let self = this;
            // self.$store.commit("addToken",tokey)//把token信息放到vuex中
            self.$axios.get('/api/ApiTestReport/loadReportData',{//请求接口数据
                params:{
                    'testReportId':testReportId
                }
            }).then(res => {
                if(res.data.statusCode==2000){
                    self.RomeData.TopData.reportName = res.data.topData.reportName;
                    self.RomeData.TopData.createTime = res.data.topData.createTime;
                    self.RomeData.TopData.runningTime = res.data.topData.runningTime+'s';
                    self.RomeData.TopData.reportStatus = res.data.topData.reportStatus;

                    self.RomeData.TopData.passTotal = res.data.topData.passTotal;
                    self.RomeData.TopData.failTotal = res.data.topData.failTotal;
                    self.RomeData.TopData.errorTotal = res.data.topData.errorTotal;

                    self.BarChart();
                    self.PieChart(res.data.topData.passRate);


                    // //新版数据加载
                    // res.data.dataTable.forEach(d=>{
                    //     let obj = {};
                    //     let lebel = d.name;
                    //     if(d.issuccess==1){
                    //         lebel='<失败>---'+d.name
                    //     }else if(d.issuccess==2){
                    //         lebel='<错误>---'+d.name
                    //     }
                    //     obj.id = d.id;
                    //     obj.name = String(d.id);
                    //     obj.label = lebel;
                    //     obj.issuccess = d.issuccess;

                    //     self.NewRomeData.firstMenu.push(obj);
                    // });
                }
                else{
                    self.$message.error('报告获取失败:'+ res.data.errorMsg);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
    }
};
</script>

<style>
.flex-layout{
    /* text-align:center;
    float:center; */
    margin:0 auto;
    width:1700px; 
}
.TopTitle{
    text-align:left;
    margin-left: 50px;
}
.TopMargin{
    margin:5px 0;
}
.EchartContainer-bar{
    width:600px; 
    height:270px;
} 
.EchartContainer-pie{
    width:600px; 
    height:270px;
}
</style>