<template>
  <div class="main-canvas">
    <div class="title1">您的测试结果</div>
    <div class="step-box">
      <el-steps :active="5" finish-status="success" align-center>
        <el-step title="量表填写" />
        <el-step title="情绪图片观看" />
        <el-step title="文字朗读" />
        <el-step title="人脸图片描述" />
        <el-step title="机器人访谈" />
        <el-step id="result-step" title="您的结果" />
      </el-steps>
    </div>
    <div class="main-box">
      <div class="main-box-text-box">
        <div class="result-text">您的抑郁症测试结果为：</div>
        <div class="result-text-title" style="margin-top: 4px">{{ this.resultDegree }}</div>
      </div>
      <div class="doctor-button" v-show="this.needDoctor">
        <i class="bi bi-info-circle" style="margin-right: 1vw;"></i>
        建议就医
      </div>
    </div>
    <div class="multifunctional-box">
      <div class="score-box">
        <div class="score-text">测试分数：</div>
        <div class="score-text-title">{{this.resultScore}}/27</div>
      </div>
      <div class="function-button-vertical-group">
        <div class="function-button-horizontal-group">
          <div class="function-button">打印结果报告</div>
          <div class="function-button">将结果发至邮箱</div>
        </div>
        <div class="function-button-horizontal-group" style="margin-top: 0.9vh">
          <div class="function-button">回顾作答情况</div>
          <div class="function-button">重新参与测试</div>
        </div>
      </div>
      <!--
      <div class="function-button-vertical-group">
        <div class="function-button">打印结果报告</div>
        <div class="function-button" style="margin-top: 1vh">回顾作答情况</div>
      </div>
      <div class="function-button-vertical-group">
        <div class="function-button">将结果发至邮箱</div>
        <div class="function-button" style="margin-top: 1vh">重新参与测试</div>
      </div>
      -->
    </div>
    <div class="text-box1">
      您的测试分数处于{{this.section}}分区间，指示您<span id="green-span">{{this.resultDegree}}</span>。{{this.recommendation}}。若您正处于或您了解有人处于自杀危机之中，可以拨打<span>400-161-9995</span>或<span>120</span>获取专业的帮助。
    </div>
    <div class="text-box2">
      一般来说，抑郁症不是一种患者可以自行治疗的疾病。但是，自助方案也能带来很大的帮助。除了谨遵医嘱坚持专业治疗外，以下方案也能够帮助您缓解症状：
      <ul class="text-ul">
        <li class="text-li">全方位了解抑郁症，可以鼓励您的家人和您一起，让您获得更好的理解和支持。</li>
        <li class="text-li">养成记录症状的习惯，便于监控康复过程中的警告或危险信号。</li>
        <li class="text-li">尝试从饮食、运动、睡眠等角度调节生活方式，避免饮酒和使用其他成瘾物质，减少咖啡因摄入，同时获取更多的维生素D。</li>
      </ul>
    </div>
    <!--
      <div class="text-box3">
        *注：检测结果需排除双向情感障碍、正常的丧亲之痛和导致抑郁症的医学障碍等情况，才能作出最终判断。
      </div>
      -->

    <div class="title2">帮助与干预</div>
    <div class="post-info-box">
      <div class="title3">常见问题及资源链接</div>
      <div class="button-horizontal-group">
        <div class="button-link">就医之前需要做好哪些准备?</div>
        <div class="button-link">患者的家属及朋友如何帮助患者康复?</div>
      </div>
      <div class="button-horizontal-group">
        <div class="button-link">抑郁症是可以治愈的吗?</div>
        <div class="button-link">自助调节方法介绍</div>
        <div class="button-link">专业治疗手段介绍</div>
      </div>
      <div class="button-horizontal-group">
        <div class="button-link">心理救助热线电话汇总</div>
        <div class="button-link">精神科医院链接</div>
      </div>
    </div>
  </div>
</template>

<script>
import {ipAddress} from "../utils.js";

export default {
  name: "ResultPage",
  data(){
    return{
      resultDegree: '可能患有中重度抑郁症',
      resultScore: 16,
      needDoctor: true,
      section: '15-19',
      recommendation: '建议您及时就医，并且需要保证积极的心理、药物或联合治疗'
    }
  },
  methods:{
    getResultScore(){
      fetch(`http://${ipAddress}/calculate-result`, {
        method: 'get',
      })
          .then(x => x.json())
          .then(x => {
            console.log(x);
            this.resultScore = x;
            this.calculateAttributeByScore();
          })
    },
    calculateAttributeByScore(){
      if(this.resultScore >= 20 && this.resultScore <= 27){
        this.resultDegree = '可能患有重度抑郁症';
        this.recommendation = '建议您及时就医，并且需要保证积极的心理、药物或联合治疗'
        this.section = '20-27';
        this.needDoctor = true;
      }else if(this.resultScore >= 15 && this.resultScore <= 19){
        this.resultDegree = '可能患有中重度抑郁症'
        this.recommendation = '建议您及时就医，并且需要保证积极的心理、药物或联合治疗'
        this.section = '15-19';
        this.needDoctor = true;
      }else if(this.resultScore >= 10 && this.resultScore <= 14){
        this.resultDegree = '可能患有中度抑郁症'
        this.recommendation = '需要根据临床诊断（如症状时间和功能损害等）确定治疗的必要性'
        this.section = '10-14';
        this.needDoctor = false;
      }else if(this.resultScore >= 5 && this.resultScore <= 9){
        this.resultDegree = '可能患有轻微抑郁症'
        this.recommendation = '需要根据临床诊断（如症状时间和功能损害等）确定治疗的必要性'
        this.section = '5-9';
        this.needDoctor = false;
      }else{
        this.resultDegree = '很少或完全没有抑郁'
        this.recommendation = '建议您经常监控自己的状态，可能无需治疗'
        this.section = '0-4';
        this.needDoctor = false;
      }
    },
  },
  mounted() {
    this.getResultScore();
  }
}
</script>

<style scoped>
@import "stylesheet/result-page.css";

</style>