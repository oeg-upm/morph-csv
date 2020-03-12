package es.upm.fi.dia.oeg.translation;

import es.upm.dia.oeg.Yarrrml2rmlc;
import es.upm.fi.dia.oeg.model.RMLCMapping;
import es.upm.fi.dia.oeg.model.YarrrmlMapping;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class yarrrml2RMLC {
    private static final Logger _log = LoggerFactory.getLogger(yarrrml2RMLC.class);

    public static RMLCMapping translateYarrrml2RMLC(YarrrmlMapping ymapping){
        String rmlcContent = Yarrrml2rmlc.translateYarrrml2RMLC(ymapping.getContent());
        _log.info("Loading RMLC mapping in RMLC-API");
        RMLCMapping rmlcMappingY = new RMLCMapping(rmlcContent);
        return rmlcMappingY;
    }

}
