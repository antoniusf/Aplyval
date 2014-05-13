varying vec4 fragcolor;

void main()
{
    gl_FrontColor = gl_Color;
    gl_BackColor = gl_Color;
    fragcolor = gl_Color;
    vec4 pos = gl_ModelViewMatrix * gl_Vertex;
    gl_Position = gl_ProjectionMatrix * pos;
}
