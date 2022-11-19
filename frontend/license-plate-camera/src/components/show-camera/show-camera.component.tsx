import { LicensePlate } from "../../interfaces/license-plate";

interface ShowCameraProps{
    url: string;
    license_plates: LicensePlate[] 
}

export default function ShowCamera(props: ShowCameraProps){
    var {url,license_plates} = props;

    return(
    <>
        <img src={url} width="50%"/>
        {/* <ul>
            {license_plates===undefined?(<>Not plates</>):(license_plates.map((plate,i)=>(
                <li>
                    {plate.plate}
                </li>
            )))}
        </ul> */}
        {/* {url}    */}
        {/* {console.log(typeof license_plates)} */}
        <pre className="section">{JSON.stringify(license_plates, null, ' ')}</pre>
    </>
    );
}