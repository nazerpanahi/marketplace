import {useState, useEffect} from 'react';
import { Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import './Categories.css'
// import { BsHouseDoorFill, BsFillHouseFill, BsFillPuzzleFill } from 'react-icons/bs'
// import { AiFillCar } from 'react-icons/ai';
// import { GiFlowerPot, GiClothes } from 'react-icons/gi';
import { TiSortAlphabetically } from 'react-icons/ti';
// import { MdPhoneAndroid } from 'react-icons/md'
import { getAll } from '../../services/categoriesData'

function CategoriesNav() {
    let [categories, setCategories] = useState([]);

    useEffect(() => {
      async function getCategories() {
        const result = await getAll();
        setCategories(result.categories);
      }
      getCategories();
    }, []);

    return (
        <div className="container" id="categories">
            <h1>Categories</h1>
            <Link to="/categories/all">
                <Button variant="dark" id="all"><TiSortAlphabetically />All</Button>{' '}
            </Link>
            {categories.map((c) =>
              <Link to={"/categories/".concat(c.title)}>
                <Button variant="dark" id={c.title}>{c.title}</Button>{' '}
              </Link>
            )}
        </div>
    )
}

export default CategoriesNav;
