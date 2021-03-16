import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button{
    id: customToggleBtn
    property url btnIconSource: "../../Images/svg_images/menu_icon.svg"
    property color colorDefault: "#000000"
    property color colorMouseOver: "#2e3836"
    property color colorPressed: "#a30000"
    QtObject{
        id: internal

        property var dynamicColor: if(customToggleBtn.down){
                                       customToggleBtn.down ? colorPressed : colorDefault
                                   }else{
                                       customToggleBtn.hovered ? colorMouseOver : colorDefault
                                   }
    }

    implicitWidth: 50
    implicitHeight: 50
    background: Rectangle{
        id: bgBtn
        color: internal.dynamicColor

        Image{
            id: iconBtn
            source: btnIconSource
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            height: 30
            width: 30
            fillMode: Image.PreserveAspectFit
        }
        ColorOverlay{
            anchors.fill: iconBtn
            source: iconBtn
            color: "#f5f5f5"
            antialiasing: false
        }
    }
}



/*##^##
Designer {
    D{i:0;formeditorZoom:3}
}
##^##*/
