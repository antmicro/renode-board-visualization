FROM antmicro/renode as RENODE_WITH_DEMO

# Bring demo assets into container
# NOTE: default renode image uses /home/developer (at time of coding) as default directory
COPY ./ /home/developer/

WORKDIR /home/developer

FROM RENODE_WITH_DEMO as blinky
CMD ["renode", "scripts/blinky.resc"]

FROM RENODE_WITH_DEMO as person
CMD ["renode", "scripts/person_detection.resc"]

