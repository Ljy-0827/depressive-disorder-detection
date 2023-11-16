<template>
  <div class="step-box-bg">
    <!-- 包含量表测评 进度条 -->
    <div class="step-box" v-if="this.activeStep === 4">
      <el-steps :active="this.activeStep" finish-status="success" align-center>
        <el-step title="量表填写" />
        <el-step title="情绪图片观看" />
        <el-step title="文字朗读" />
        <el-step title="人脸图片描述" />
        <el-step id="result-step" title="机器人访谈" />
        <el-step title="您的结果" />
      </el-steps>
    </div>
    <!-- 不包含量表测评 进度条 -->
    <div class="step-box" v-if="this.activeStep === 3">
      <el-steps :active="this.activeStep" finish-status="success" align-center>
        <el-step title="量表填写" />
        <el-step title="情绪图片观看" />
        <el-step title="文字朗读" />
        <el-step title="人脸图片描述" />
        <el-step id="result-step" title="机器人访谈" />
        <el-step title="您的结果" />
      </el-steps>
    </div>
  </div>
  <div class="main-title">机器人访谈</div>
  <div class="avatar-box"></div>
  <div class="explain-box" v-show="!isBeginInterview">
    <div class="explain-box-left">
      <div class="explain-box-left-text">
        请您按照上方视频的引导，完成访谈内容。您可以在没有进入下一个话题之前修改您的回答。
      </div>
    </div>
    <div class="explain-box-right">
      <button class="open-mic-button" v-if="!isMicOpen" @click="openMic">打开麦克风</button>
      <div class="open-mic-countdown" v-if="!isMicOpen">音频将在{{this.countdown}}秒后自动开启</div>
      <button class="begin-interview-button-small" v-if="isMicOpen" @click="startInterview">开始访谈</button>
    </div>
  </div>
  <div class="chat-box" v-show="isBeginInterview">
    <el-scrollbar>
      <div class="question-and-answer" v-for="item in this.questionAndAnswer">
        <div class="question-box" v-show="item.isReadyShow === true">
          <div class="question-avatar"></div>
          <div class="question-text">{{ item.question }}</div>
        </div>
        <div class="answer-box" v-show="item.answer !== 0">
          <div class="answer-mix" disabled="item.status" @click="onClickAudio">
            <i class="bi bi-play-fill" style="margin-right: 9vw" v-show="!item.status && !this.isPlaying"></i>
            <i class="bi bi-pause-fill" style="margin-right: 9vw" v-show="!item.status && this.isPlaying"></i>
            <i class="bi bi-check" style="margin-right: 9vw" v-show="item.status"></i>
            {{item.answer}}''
            <i class="bi bi-soundwave" style="margin-left: 2vw"></i>
          </div>
          <div class="answer-avatar"></div>
        </div>
      </div>
    </el-scrollbar>
  </div>
  <div class="begin-interview-button" @click="startInterview" v-if="!isBeginInterview">开始访谈</div>
  <div class="begin-recording-button" @click="startRecording" v-if="isBeginInterview && !isRecording && !isWaitingCheck">开始回答</div>
  <div class="stop-recording-button" @click="stopRecording" v-if="isBeginInterview && isRecording">结束回答</div>
  <div class="button-group">
    <div class="begin-recording-again-button" @click="startRecordingAgain" v-if="isWaitingCheck && !isRecording">重新录制</div>
    <div class="allow-next-question" @click="moveToNextQuestion" v-if="isWaitingCheck && !isRecording">提交回答</div>
  </div>
</template>

<script>
import {interviewQuestions, ipAddress} from "../utils.js";
import {ElMessage} from "element-plus";

export default {
  name: "Step5Interview",
  data(){
    return{
      isMicOpen: false,
      audioChunks: [],
      audioUrl: null,
      mediaRecorder: null,
      countdown: 3,
      isBeginInterview: false,
      questionAndAnswer:[],
      isRecording: false,
      questionAnswering: 0,
      recordingStartTime: null,
      tmpSeconds: 0,
      isWaitingCheck: false,
      isPlaying: false,
      audioElement: null,

      includeQuestionnaire: true,
      activeStep: 4,
    }
  },

  mounted() {
    this.includeQuestionnaire = this.$route.query.includeQuestionnaire;
    if(this.includeQuestionnaire === true){
      this.activeStep = 4;
    }else{
      this.activeStep = 3;
    }
    this.startCountdown();
    this.initialQuestionAndAnswer();
  },

  methods:{
    initialQuestionAndAnswer(){
      for(let i = 0; i < 18; i++){
        this.questionAndAnswer.push({question: interviewQuestions[i], answer: 0, isReadyShow: false})
      }
      console.log(this.questionAndAnswer);
    },
    startCountdown() {
      this.countdown = 3; // 设置初始值为3
      this.timer = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
        } else {
          clearInterval(this.timer); // 清除计时器
          this.openMic();
        }
      }, 1000); // 每秒执行一次
    },
    openMic(){
      return navigator.mediaDevices
          .getUserMedia({ audio: true })
          .then((stream) => {
            this.stream = stream;
            this.isMicOpen = true;
          });
    },
    startInterview(){
      this.isBeginInterview = true;
      this.questionAndAnswer[0].isReadyShow = true;
    },
    startRecording(){
      navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
        this.isRecording = true;
        this.audioChunks = [];
        this.mediaRecorder = new MediaRecorder(stream);
        this.mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            this.audioChunks.push(event.data);
          }
        };
        this.mediaRecorder.onstop = () => {
          this.isRecording = false;
          const audioBlob = new Blob(this.audioChunks, { type: "audio/wav" });
          this.audioUrl = URL.createObjectURL(audioBlob);
          console.log("create:", this.audioUrl)
        };
        this.mediaRecorder.start();
        this.recordingStartTime = new Date(); // 记录开始录制的时间戳
      });
    },
    stopRecording(){
      if (this.mediaRecorder && this.isRecording) {
        this.mediaRecorder.stop();
      }
      if (this.recordingStartTime) {
        const endTime = new Date();
        const seconds = Math.round((endTime - this.recordingStartTime) / 1000);
        this.tmpSeconds = seconds;
      }
      this.questionAndAnswer[this.questionAnswering].answer = this.tmpSeconds;
      this.isWaitingCheck = true;
      //console.log(this.questionAndAnswer[this.questionAnswering].answer);
    },
    startRecordingAgain(){
      this.audioChunks = [];
      this.audioUrl = null;
      this.mediaRecorder = null;
      this.audioElement = null;
      this.startRecording();
    },
    async sendAudioToBackend() {
      try {
        const blob = new Blob(this.audioChunks, {type: 'audio/wav'});
        const formData = new FormData();
        formData.append('audio', blob, `interview${this.questionAnswering + 1}_audio.wav`);

        const response = await fetch(`http://${ipAddress}/upload-audio`, {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          ElMessage({
            message: '录音已成功上传',
            type: 'success',
          });
          this.isUploading = false;
          if(this.questionAnswering === this.questionAndAnswer.length - 1){
            this.$router.push('/result');
          }
          //this.$router.push({name: 'step-complete', query: {currentPage: '4'}});
        } else {
          ElMessage.error('录音上传失败');
          this.isUploading = false;
        }
      } catch (error) {
        ElMessage.error('录音上传失败');
        this.isUploading = false;
      }
    },
    moveToNextQuestion(){
      this.sendAudioToBackend();
      this.questionAndAnswer[this.questionAnswering].status = true;
      this.questionAnswering ++;
      this.questionAndAnswer[this.questionAnswering].isReadyShow = true;
      this.isWaitingCheck = false;
      this.audioChunks = [];
      this.audioUrl = null;
      this.mediaRecorder = null;
      this.audioElement = null;
    },
    onClickAudio(){
      if (this.isPlaying) {
        if (this.audioElement && this.isPlaying) {
          this.audioElement.pause();
          this.isPlaying = false;
        }
      } else {
        console.log("status:", this.audioUrl);
        if (this.audioUrl && !this.isPlaying) {
          if (this.audioElement) {
            this.audioElement.pause(); // 先暂停任何正在播放的音频
          }

          this.audioElement = new Audio(this.audioUrl);
          this.audioElement.addEventListener("ended", () => {
            this.isPlaying = false;
          });
          this.audioElement.play();
          this.isPlaying = true;
        }

      }
    }
  }
}
</script>

<style scoped>
@import "stylesheet/step5-interview.css";
</style>