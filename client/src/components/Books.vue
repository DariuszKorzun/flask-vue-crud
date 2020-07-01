<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-12">

        <h1>Products</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.product-modal>Add Product</button>
        <br><br>

        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Product</th>
              <th scope="col">Name</th>
              <th scope="col">Developer</th>
              <th scope="col">Created</th>
              <th scope="col">Category</th>
              <th scope="col">Subcategory</th>
              <th scope="col">Type</th>
              <th scope="col">Website</th>
              <th scope="col">Documentation</th>
              <th scope="col">Modified</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
                  <tr v-for="(product, index) in products" :key="index">
                            <td>{{ index }} </td>
                            <td>{{ product.fullname }}</td>
                            <td>{{ product.developer }}</td>
                            <td>{{ product.created }}</td>
                            <td>
                              <ul id="product.category">
                                <li v-for="category in product.category" :key="category">
                                  {{ category }}
                                </li>
                              </ul>
                            </td>
                            <td>
                              <ul>
                                <li v-for="subcategory in product.subcategory" :key="subcategory">
                                  {{ subcategory }}
                                </li>
                              </ul>
                            </td>
                            <td>
                              <ul>
                                <li v-for="type in product.type" :key="type">
                                  {{ type }}
                                </li>
                              </ul>
                            </td>
                            <td><a :href=product.website>{{ product.website }}</a></td>
                            <td><a :href=product.documentation>{{ product.documentation }}</a></td>
                            <td>{{ product.modified }}</td>
                            <td>
                                <div class="btn-group" role="group">
                                  <button
                                          type="button"
                                          class="btn btn-warning btn-sm"
                                          v-b-modal.product-update-modal
                                          @click="editProduct(product)">
                                      Update
                                  </button>
                                  <button
                                          type="button"
                                          class="btn btn-danger btn-sm"
                                          @click="onDeleteProduct(product)">
                                      Delete
                                  </button>
                                </div>

                              </td>
                  </tr>
          </tbody>

        </table>

      </div>
    </div>

    <b-modal ref="addProductModal"
            id="product-modal"
            title="New product"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-productname-group"
            label="Product name:"
            label-for="form-productname-input">
            <b-form-input id="form-productname-input"
                          type="text"
                          v-model="addProductForm.productname"
                          required
                          placeholder="Enter title">
            </b-form-input>
        </b-form-group>
        <b-form-group id="form-title-group"
            label="Title:"
            label-for="form-title-input">
            <b-form-input id="form-title-input"
                          type="text"
                          v-model="addProductForm.title"
                          required
                          placeholder="Enter title">
            </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
            label="Author:"
            label-for="form-author-input">
            <b-form-input id="form-author-input"
                          type="text"
                          v-model="addProductForm.author"
                          required
                          placeholder="Enter author">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-read-group">
          <b-form-checkbox-group v-model="addProductForm.read" id="form-checks">
            <b-form-checkbox value="true">Read?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>

    <b-modal ref="editProductModal"
            id="product-update-modal"
            title="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-title-edit-group"
                    label="Title:"
                    label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="Author:"
                      label-for="form-author-edit-input">
            <b-form-input id="form-author-edit-input"
                          type="text"
                          v-model="editForm.author"
                          required
                          placeholder="Enter author">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-read-edit-group">
          <b-form-checkbox-group v-model="editForm.read" id="form-checks">
            <b-form-checkbox value="true">Read?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>

  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      products: [],
      dictionaries: [],
      keys: [],
      addProductForm: {
        title: '',
        author: '',
        read: [],
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        title: '',
        author: '',
        read: [],
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getProducts() {
      const path = 'http://localhost:5000/products';
      axios.get(path)
        .then((res) => {
          this.products = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getDictionaries() {
      const path = 'http://localhost:5000/dictionaries';
      axios.get(path)
        .then((res) => {
          this.dictionaries = function(){return Object.keys(res.data).sort().reduce((r,k)=>(r[k]=o[k],r),{})};
          // eslint-disable-next-line
          console.log(res.data);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addProduct(payload) {
      const path = 'http://localhost:5000/products';
      axios.post(path, payload)
        .then(() => {
          this.getProducts();
          this.message = 'Product added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getProducts();
        });
    },
    initForm() {
      this.addProductForm.title = '';
      this.addProductForm.author = '';
      this.addProductForm.read = [];
      this.editForm.id = '';
      this.editForm.title = '';
      this.editForm.author = '';
      this.editForm.read = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addProductModal.hide();
      let read = false;
      if (this.addProductForm.read[0]) read = true;
      const payload = {
        title: this.addProductForm.title,
        author: this.addProductForm.author,
        read, // property shorthand
      };
      this.addProduct(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addProductModal.hide();
      this.initForm();
    },
    editProduct(product) {
      this.editForm = product;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editProductModal.hide();
      let read = false;
      if (this.editForm.read[0]) read = true;
      const payload = {
        title: this.editForm.title,
        author: this.editForm.author,
        read,
      };
      this.updateProduct(payload, this.editForm.id);
    },
    updateProduct(payload, productID) {
      const path = `http://localhost:5000/products/${productID}`;
      axios.put(path, payload)
        .then(() => {
          this.getProducts();
          this.message = 'Product updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getProducts();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editProductModal.hide();
      this.initForm();
      this.getProducts(); // why?
    },
    removeProduct(productID) {
      const path = `http://localhost:5000/products/${productID}`;
      axios.delete(path)
        .then(() => {
          this.getProducts();
          this.message = 'Product removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getProducts();
        });
    },
    onDeleteProduct(product) {
      this.removeProduct(product.id);
    },
  },
  created() {
    this.getProducts();
    this.getDictionaries();
  },
};
</script>
