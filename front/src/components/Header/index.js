import './Header.css';
import Link from "../Link";

const Header = () => {
    return (
        <header className='header'>
            <img src="/img/header.png" alt="imagem da pagina princapal." />
            <h1>Seja bem vindo a RPM Esports!</h1>
            <h2>Seu Clube, Sua liga no Automobilismo Virtual do Brasil. </h2>
            <Link link="https://google.com" texto="Whatsapp" cor="#FFF"/>
            <Link link="https://youtube.com" texto="Youtube" cor="000"/>
        </header>
    )
}

export default Header;