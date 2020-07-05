<template>
  <div class="upload-img">
    <el-card>Flask Vue 图片识别</el-card>
    <br />
    <el-card>
      <el-row>
        <el-col :span="12">
          <el-radio v-model="recon_option" size="small" label="car" border>车牌识别</el-radio>
          <el-radio v-model="recon_option" size="small" label="barcode" border>二维码条码识别</el-radio>
        </el-col>
        <el-col :span="6">
          <el-upload
            class="upload-demo"
            action="/recon_pic"
            :show-file-list="false"
            :data="postOption"
            :before-upload="onBeforeUpload"
          >
            <el-tooltip class="item" effect="dark" content="只能上传jpg/png文件" placement="bottom">
              <el-button size="small" type="primary">点击上传</el-button>
            </el-tooltip>
          </el-upload>
        </el-col>
        <el-col :span="6">
          <el-button size="small" @click="onUpload" type="primary">开始识别</el-button>
        </el-col>
      </el-row>
    </el-card>
    <br />
    <el-card>
      <h4 v-if="this.file">图片：{{this.file.name}}</h4>
      <h4 v-else>请选择图片识别</h4>

      <div v-for="item in result.text" v-bind:key="item">
        <p>{{item}}</p>
      </div>
      <div v-for="(item,index) in result.pic" v-bind:key="index">
        <img style="width: 70%;" :src="'data:image/png;base64,' + item" />
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UploadImg",
  data() {
    return {
      recon_option: "car",
      file: null,
      result: {}
    };
  },
  computed: {
    postOption() {
      return {
        recon_option: this.recon_option
      };
    }
  },
  methods: {
    onBeforeUpload(file) {
      this.file = file;
      this.result = {};
      return this._initPromResolve();
    },
    _initPromResolve() {
      return (this.prom = new Promise(resolve => (this.promResolve = resolve)));
    },
    onUpload() {
      if (!this.recon_option) {
        this.$message({
          showClose: true,
          message: "请选择识别类型",
          type: "warning"
        });
        return;
      }
      if (!this.file) {
        this.$message({
          showClose: true,
          message: "请选择文件",
          type: "warning"
        });
        return;
      }
      const loading = this.$loading({ text: "正在识别..." });
      let formData = new FormData();
      formData.append("recon_option", this.recon_option);
      formData.append("image", this.file);
      axios
        .post("/recon_pic", formData, {
          headers: { "Content-Type": "multipart/form-data" }
        })
        .then(res => {
          loading.close();
          this.result = res.data;
          if (!this.result | (this.result.code != 200)) {
            this.$message({
              showClose: true,
              message: this.result.message,
              type: "error"
            });
          } else {
            this.$message({
              showClose: true,
              message: "识别成功",
              type: "success"
            });
          }
        })
        .catch(err => {
          loading.close();
          this.$message({
            showClose: true,
            message: err,
            type: "error"
          });
        });
    }
  }
};
</script>

