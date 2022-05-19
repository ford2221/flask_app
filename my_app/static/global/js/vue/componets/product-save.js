Vue.component('product-save',{
    props: {
        time: Number,
        productEdit: {
            type: Object,
            //default: undefined
        } 
    },
    data: function(){
        return {
            products: [],
            fname: "",
            fprice: 0,
            fcategory_id: 0,
            product: "",
            error: "",
            categories: []
            
        }
    },
    created(){
        this.getCategories()
    },
    methods: {
        getCategories: function(){
            fetch('http://localhost:5000/api/category/')
            .then(res => res.json())
            .then(res => {

                this.categories = res.data           
            })
        },
        productSave: function(){
            var formData = new FormData()
            formData.append("name", this.fname)
            formData.append("price", this.fprice)
            formData.append("category_id", this.fcategory_id)
            this.error = ""

            if (this.productEdit) {
                this.productUpdate(formData)
            }else{
                this.productInsert(formData)
            }
            
        },
        productInsert(formData){
            fetch('http://localhost:5000/api/product/', {
                method: 'POST',
                body: formData
            })
            .then(res => res.json())
            .then(res => {
                if (res.code == 200){
                    this.product = res
                    this.$emit("eventProductInsert", this.product);
                }else{
                    this.error = res.msg
                }
                
            })
        },
        productUpdate(formData){
            fetch('http://localhost:5000/api/product/'+this.productEdit.id, {
                method: 'PUT',
                body: formData
            })
            .then(res => res.json())
            .then(res => {
                if (res.code == 200){
                    this.product = res
                    this.$emit("eventProductUpdate", this.product);
                }else{
                    this.error = res.msg 
                }
            })
        }
    },
    watch: {
        time: function(newValue, oldValue){
            //console.log(this.time+"  "+this.product);
            this.error = ""
            if (this.productEdit) {
                this.fname = this.productEdit.name
                this.fprice = this.productEdit.price
                this.fcategory_id = this.productEdit.category_id
            } else {
                this.fname = ""
                this.fprice = 0
                this.fcategory_id = 0
            }
                        
        }
    },
    template:
    `
        <div  class="modal fade" id="saveModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div  class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Crear producto</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">

                        <div v-if="error" class="alert alert-danger">
                            {{ error }}
                        </div>

                        <div class="form-group">
                            <label for="name">Nombre</label> 
                            <input class="form-control" v-model="fname" type="text" value="">
                        
                        </div>
                        
                        <div class="form-group">
                            <label for="price">Precio</label> 
                            <input class="form-control" v-model="fprice" type="text" value="">
                        
                        </div>
                        
                        <div>
                            <label for="category_id">Categoria</label> 
                            <select class="form-control" v-model="fcategory_id"> 
                                <option v-for="c in categories" value="c.id">{{ c.name }}</option>
                            </select>
                        </div>

                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button v-on:click="productSave" class="btn btn-success" data-bs-dismiss="modal">Enviar</button>
                        
                    </div>
                </div>
            </div>
            
        </div>
    `
});

