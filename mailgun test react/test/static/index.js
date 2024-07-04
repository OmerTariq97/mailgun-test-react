const app = new Vue({
    el:'#vm',
    delimiters: ['[[', ']]'],
    data:{
        articles:[]
    },
    mounted() {
        this.loadArticles();
      },
      created:function() {
        this.loadArticles();
      },
    methods:{
    loadArticles() {
        this.articles=[1,2,3]
        }
    }

    })