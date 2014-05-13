varying vec4 fragcolor;

void main()
{
    vec4 color = fragcolor;
    float d = 1.0 - color.a;
    float a = (1.0/d) / 200.0 ;
    gl_FragColor = vec4(color.xyz, a);
}
