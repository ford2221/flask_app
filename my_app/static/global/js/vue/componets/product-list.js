Vue.component('product-list',{
    data: function(){
        return {
            products: [],
            productSelected: undefined,
            productIndexSelected: 0, 
            timeDelete:0,
            timeSave:0,
        }
    },
    mounted(){
        this.findall();
    },
    methods: {
        findall: function(){
            console.log('hola log');
            this.message = 'you gave me click'

            fetch('http://localhost:5000/api/product/')
            .then(res => res.json())
            .then(res => this.products = res );
        },
        productDelete: function(product,index){
            this.timeDelete = new Date().getTime()
            this.productSelected = product;
            this.productIndexSelected = index;
        },
        productSave: function(){
            this.productSelected = undefined
            this.timeSave = new Date().getTime()
        },
        productUpdate: function(product,index){
            this.timeSave = new Date().getTime()
            this.productSelected = product;
            this.productIndexSelected = index;
        },
        eventProductDelete: function(){
            console.log('deleted');
            this.$delete(this.products.data, this.productIndexSelected)
        },
        eventProductInsert: function(product){
            console.log(product.data.name);
            this.products.data.push(product.data)
        },
        eventProductUpdate: function(product){
            this.products.data[this.productIndexSelected].name = product.data.name
            this.products.data[this.productIndexSelected].price = product.data.price
            this.products.data[this.productIndexSelected].category = product.data.category
            this.products.data[this.productIndexSelected].category_id = product.data.category_id

            
        }
    },
    
    template:
    `
        <div>
            <button class="btn btn-success" v-on:click="productSave" data-bs-toggle="modal" data-bs-target="#saveModal">Crear</button>
            <div v-if="products.length == 0">
                <h1>No products</h1>
            </div>
            <div v-else>
                <h1>Productos</h1>
            </div>

            <div v-for='(product, index) in products.data' class=" mt-3 mb-3 pb-2 pt-3 ">

                <h3>
                    <a href="#">
                        {{ product.name }} 
                    </a>
                </h3>

                <h5>{{ product.category }}</h5>

                <a v-on:click="productUpdate(product,index)" class="btn btn-info btn-sm" data-bs-toggle="modal" 
                    data-bs-target="#saveModal" title="Editar"
                    href="#">
                    <i class="fa fa-edit"> </i>
                </a>
                <button  v-on:click="productDelete(product,index)" data-bs-toggle="modal" data-bs-target="#deleteModal" :data-name="product.name"
                    data-bs-placement="top" title="Eliminar" :data-id="product.id" class="btn btn-danger btn-sm" >
                    <i class="fa fa-trash"></i> 
                </button> 
            </div>
            <product-delete v-on:eventProductDelete="eventProductDelete" :time="timeDelete" :product="productSelected">
            </product-delete>

            
            <product-save v-on:eventProductUpdate="eventProductUpdate" v-on:eventProductInsert="eventProductInsert"
                 :productEdit="productSelected" :time="timeSave">
            </product-save>
        </div>
    `
});

