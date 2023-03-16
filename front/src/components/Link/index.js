import './Link.css';

const Link = ({link, texto, cor}) => {
    return (
        <div classname='link' style={{backgroundColor: cor}}>
            <a href={link}>
                {texto}
            </a>
        </div>
    )
}

export default Link;