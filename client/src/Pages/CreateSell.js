import { useEffect, useState } from 'react';
import { Form, Button, Col, Spinner, Alert } from 'react-bootstrap';
import { createProduct } from '../services/productData';
import SimpleSider from '../components/Siders/SimpleSider';
import '../components/CreateSell/CreateSell.css';
import { getAll } from '../services/categoriesData';

// class AddProduct extends Component {
function AddProduct({ history }) {
    let [title, setTitle] = useState("");
    let [price, setPrice] = useState(0);
    let [description, setDescription] = useState("");
    let [city, setCity] = useState("");
    let [category, setCategory] = useState("");
    let [image, setImage] = useState("");
    let [loading, setLoading] = useState(false);
    let [alertShow, setAlertShow] = useState(false);
    let [errors, setErrors] = useState("");
    let [categories, setCategories] = useState([]);

    const onSubmitHandler = (e) => {
        e.preventDefault();
        let obj = { title, price, description, city, category }
        setLoading(true);
        if (!!image) {
            getBase64(image)
                .then((data) => {
                    obj['image'] = data;
                })
                .catch(err => console.error('Converting to base64 err: ', err));
        }
        let token = localStorage.getItem('token')
        createProduct(obj, token)
            .then(res => {
                if (res.error) {
                    setLoading(false);
                    setErrors(res.error);
                    setAlertShow(true);
                } else {
                    history.push(`/categories/${category}/${res.productId}/details`)
                }
            })
            .catch(err => console.error('Creating product err: ', err))
    }

    useEffect(() => {
        async function getCategories() {
            const result = await getAll();
            let categories = result.categories.map((item) => ({ ...item, "key": item.id }))
            setCategories(categories);
        }
        getCategories();
    }, []);

    const getBase64 = (file) => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result);
            reader.onerror = error => reject(error);
        });
    }

    return !localStorage.getItem('token') ?
            (
                <>
                    {history.push('/')}
                </>
            )
            :
            (
                <>
                    <SimpleSider />
                    <div className='container'>
                        <h1 className="heading">Add a Product</h1>
                        <Form onSubmit={onSubmitHandler}>
                            {alertShow &&
                                <Alert variant="danger" onClose={setAlertShow(false)} dismissible>
                                    <p>
                                        {errors}
                                    </p>
                                </Alert>
                            }
                            <Form.Row>
                                <Form.Group as={Col} controlId="formGridTitle">
                                    <Form.Label>Title</Form.Label>
                                    <Form.Control type="text" placeholder="Enter title" name="title" required onChange={(e) => setTitle(e.target.value)} />
                                </Form.Group>

                                <Form.Group as={Col} controlId="formGridPrice">
                                    <Form.Label>Price</Form.Label>
                                    <Form.Control type="number" step="0.01" placeholder="Price" name="price" required onChange={(e) => setPrice(e.target.value)} />
                                </Form.Group>
                            </Form.Row>

                            <Form.Group controlId="formGridDescription.ControlTextarea1">
                                <Form.Label>Description</Form.Label>
                                <Form.Control as="textarea" rows={3} name="description" required onChange={(e) => setDescription(e.target.value)} />
                            </Form.Group>

                            <Form.Row>
                                <Form.Group as={Col} controlId="formGridCity">
                                    <Form.Label>City</Form.Label>
                                    <Form.Control name="city" placeholder="Sofia" required onChange={(e) => setCity(e.target.value)} />
                                </Form.Group>

                                <Form.Group as={Col} controlId="formGridCategory">
                                    <Form.Label>Category</Form.Label>
                                    <Form.Control as="select" defaultValue="Choose..." name="category" required onChange={(e) => setCategory(e.target.value)}>
                                        <option>Choose...</option>
                                        {categories.map((c) => <option>{c.title}</option>)}
                                    </Form.Control>
                                </Form.Group>

                                <Form.Group as={Col} controlId="formGridImage" >
                                    <Form.Label>Image</Form.Label>
                                    <Form.Control name="image" type="file" onChange={(e) => setImage(e.target.files[0])} />
                                </Form.Group>
                            </Form.Row>
                            {loading ?
                                <Button className="col-lg-12" variant="dark" disabled >
                                    Please wait... <Spinner animation="border" />
                                </Button>
                                :
                                <Button className="col-lg-12" variant="dark" type="submit">Add product</Button>
                            }
                        </Form>
                    </div>
                </>
            )
}

export default AddProduct;
