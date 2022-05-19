Vue.component('product-delete',{
    props: ['product', 'time'],
    data: function(){
        return {
            products: []
            
        }
    },
    methods: {
        productDelete: function(){
            fetch('http://localhost:5000/api/product/'+this.product.id, {
                method: 'DELETE'
            })
            .then(res => res.json())
            .then(res => this.$emit("eventProductDelete"));
        }
    },
    watch: {
        time: function(newValue, oldValue){
            console.log(this.time+"  "+this.product.name);
        }
    },
    template:
    `
        <div  class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div v-if="product" class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Nombre: {{ product.name }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        ¿Seguro que desea eliminar el registro seleccionado?
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button v-on:click="productDelete" class="btn btn-danger" data-bs-dismiss="modal">Borrar</button>
                    </div>
                </div>
            </div>
            
        </div>
    `
});